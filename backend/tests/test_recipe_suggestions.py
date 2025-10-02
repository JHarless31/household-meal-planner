"""
Unit Tests for Recipe Suggestion Service
"""

from datetime import date, timedelta
from uuid import uuid4

import pytest

from src.models.inventory import InventoryItem
from src.models.rating import Rating
from src.models.recipe import Ingredient, Recipe, RecipeVersion
from src.models.user import User
from src.services.recipe_suggestions import RecipeSuggestionService


class TestRecipeSuggestionService:
    """Test cases for recipe suggestion algorithms"""

    def test_suggest_by_rotation_never_cooked_first(self, db_session, test_user):
        """Test that never-cooked recipes are suggested first"""
        # Create recipes with different cooking history
        recipe1 = Recipe(
            title="Never Cooked",
            created_by=test_user.id,
            times_cooked=0,
            last_cooked_date=None,
        )
        recipe2 = Recipe(
            title="Cooked Recently",
            created_by=test_user.id,
            times_cooked=5,
            last_cooked_date=date.today() - timedelta(days=2),
        )
        recipe3 = Recipe(
            title="Cooked Long Ago",
            created_by=test_user.id,
            times_cooked=3,
            last_cooked_date=date.today() - timedelta(days=60),
        )

        db_session.add_all([recipe1, recipe2, recipe3])
        db_session.commit()

        # Get suggestions
        suggestions = RecipeSuggestionService.suggest_by_rotation(
            db_session, test_user.id, limit=10
        )

        # Never cooked should be first
        assert len(suggestions) == 3
        assert suggestions[0]["title"] == "Never Cooked"
        assert suggestions[0]["times_cooked"] == 0
        assert suggestions[0]["reason"] == "Never tried before"

    def test_suggest_by_favorites(self, db_session, test_user):
        """Test that highly-rated recipes are suggested as favorites"""
        # Create recipes with ratings
        recipe1 = Recipe(title="Highly Rated", created_by=test_user.id)
        recipe2 = Recipe(title="Moderately Rated", created_by=test_user.id)
        db_session.add_all([recipe1, recipe2])
        db_session.flush()

        # Add ratings
        for _ in range(5):
            db_session.add(
                Rating(recipe_id=recipe1.id, user_id=test_user.id, rating=True)
            )
        for _ in range(3):
            db_session.add(
                Rating(recipe_id=recipe2.id, user_id=test_user.id, rating=True)
            )
        for _ in range(2):
            db_session.add(
                Rating(recipe_id=recipe2.id, user_id=test_user.id, rating=False)
            )
        db_session.commit()

        # Get favorite suggestions
        suggestions = RecipeSuggestionService.suggest_by_favorites(
            db_session, test_user.id, limit=10
        )

        # Highly rated should be first
        assert len(suggestions) >= 1
        assert suggestions[0]["title"] == "Highly Rated"
        assert suggestions[0]["rating_count"] == 5

    def test_suggest_never_tried(self, db_session, test_user):
        """Test never-tried suggestions only include uncooked recipes"""
        # Create mix of cooked and never-cooked recipes
        recipe1 = Recipe(title="Never Tried 1", created_by=test_user.id, times_cooked=0)
        recipe2 = Recipe(
            title="Already Cooked", created_by=test_user.id, times_cooked=1
        )
        recipe3 = Recipe(title="Never Tried 2", created_by=test_user.id, times_cooked=0)

        db_session.add_all([recipe1, recipe2, recipe3])
        db_session.commit()

        # Get suggestions
        suggestions = RecipeSuggestionService.suggest_never_tried(
            db_session, test_user.id, limit=10
        )

        # Should only include never-cooked recipes
        assert len(suggestions) == 2
        titles = [s["title"] for s in suggestions]
        assert "Never Tried 1" in titles
        assert "Never Tried 2" in titles
        assert "Already Cooked" not in titles

    def test_suggest_by_available_inventory(self, db_session, test_user):
        """Test suggestions based on inventory availability"""
        # Create recipe with ingredients
        recipe = Recipe(title="Pasta Dish", created_by=test_user.id)
        db_session.add(recipe)
        db_session.flush()

        version = RecipeVersion(
            recipe_id=recipe.id,
            version_number=1,
            instructions="Cook pasta",
            servings=4,
            modified_by=test_user.id,
        )
        db_session.add(version)
        db_session.flush()

        # Add ingredients
        ingredients = [
            Ingredient(
                recipe_version_id=version.id, name="pasta", quantity=200, unit="g"
            ),
            Ingredient(
                recipe_version_id=version.id, name="tomatoes", quantity=3, unit="pcs"
            ),
            Ingredient(
                recipe_version_id=version.id, name="cheese", quantity=100, unit="g"
            ),
        ]
        db_session.add_all(ingredients)

        # Add inventory items (2 out of 3 available)
        inventory = [
            InventoryItem(item_name="pasta", quantity=500, unit="g"),
            InventoryItem(item_name="tomatoes", quantity=5, unit="pcs"),
        ]
        db_session.add_all(inventory)
        db_session.commit()

        # Get suggestions
        suggestions = RecipeSuggestionService.suggest_by_available_inventory(
            db_session, test_user.id, limit=10, min_ingredient_match_percent=0.5
        )

        # Should suggest recipe with 66% match
        assert len(suggestions) == 1
        assert suggestions[0]["title"] == "Pasta Dish"
        assert suggestions[0]["match_percent"] > 60
        assert "cheese" in suggestions[0]["missing_ingredients"]

    def test_suggest_quick_meals(self, db_session, test_user):
        """Test quick meal suggestions filter by time"""
        # Create recipes with different cooking times
        recipe1 = Recipe(title="Quick Salad", created_by=test_user.id)
        recipe2 = Recipe(title="Slow Roast", created_by=test_user.id)
        db_session.add_all([recipe1, recipe2])
        db_session.flush()

        # Quick recipe version
        version1 = RecipeVersion(
            recipe_id=recipe1.id,
            version_number=1,
            instructions="Chop and mix",
            prep_time_minutes=10,
            cook_time_minutes=5,
            modified_by=test_user.id,
        )
        # Slow recipe version
        version2 = RecipeVersion(
            recipe_id=recipe2.id,
            version_number=1,
            instructions="Roast slowly",
            prep_time_minutes=20,
            cook_time_minutes=120,
            modified_by=test_user.id,
        )
        db_session.add_all([version1, version2])
        db_session.commit()

        recipe1.current_version = 1
        recipe2.current_version = 1
        db_session.commit()

        # Get quick meal suggestions (max 30 minutes)
        suggestions = RecipeSuggestionService.suggest_quick_meals(
            db_session, test_user.id, limit=10, max_total_time=30
        )

        # Should only include quick salad
        assert len(suggestions) == 1
        assert suggestions[0]["title"] == "Quick Salad"
        assert suggestions[0]["total_time_minutes"] == 15


# Fixtures
@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed",
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def db_session():
    """Mock database session - implement based on your test setup"""
    # This should be implemented with your actual test database setup
    # Example using SQLAlchemy:
    # from sqlalchemy import create_engine
    # from sqlalchemy.orm import sessionmaker
    # engine = create_engine('sqlite:///:memory:')
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # yield session
    # session.close()
    pass

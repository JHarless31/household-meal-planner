"""
Unit Tests for Recipe Service
Tests recipe CRUD operations, versioning, and rotation tracking
"""

from datetime import date, timedelta
from uuid import uuid4

import pytest

from src.models.recipe import Ingredient, Recipe, RecipeVersion
from src.schemas.recipe import IngredientInput, RecipeCreate, RecipeUpdate
from src.services.recipe_service import RecipeService


@pytest.mark.unit
class TestRecipeService:
    """Test cases for recipe service"""

    def test_create_recipe_success(self, db, test_user):
        """Test successful recipe creation"""
        recipe_data = RecipeCreate(
            title="New Recipe",
            description="Test description",
            prep_time_minutes=10,
            cook_time_minutes=20,
            servings=4,
            difficulty="easy",
            instructions="Test instructions",
            ingredients=[
                IngredientInput(
                    name="ingredient1", quantity=100, unit="g", category="other"
                ),
                IngredientInput(
                    name="ingredient2", quantity=200, unit="ml", category="other"
                ),
            ],
            tags=["tag1", "tag2"],
        )

        recipe = RecipeService.create_recipe(db, recipe_data, test_user.id)

        assert recipe.id is not None
        assert recipe.title == "New Recipe"
        assert recipe.current_version == 1
        assert recipe.created_by == test_user.id

        # Check version created
        version = (
            db.query(RecipeVersion)
            .filter(
                RecipeVersion.recipe_id == recipe.id, RecipeVersion.version_number == 1
            )
            .first()
        )
        assert version is not None
        assert version.prep_time_minutes == 10
        assert version.cook_time_minutes == 20

        # Check ingredients created
        ingredients = (
            db.query(Ingredient)
            .filter(Ingredient.recipe_version_id == version.id)
            .all()
        )
        assert len(ingredients) == 2

    def test_create_recipe_with_source_url(self, db, test_user):
        """Test recipe creation with source URL"""
        recipe_data = RecipeCreate(
            title="Scraped Recipe",
            description="From website",
            source_url="https://example.com/recipe",
            prep_time_minutes=15,
            cook_time_minutes=30,
            servings=2,
            difficulty="medium",
            instructions="Instructions",
            ingredients=[],
        )

        recipe = RecipeService.create_recipe(db, recipe_data, test_user.id)

        assert recipe.source_url == "https://example.com/recipe"
        assert recipe.source_type == "scraped"

    def test_get_recipe_success(self, db, test_recipe):
        """Test successful recipe retrieval"""
        recipe = RecipeService.get_recipe(db, test_recipe.id)

        assert recipe is not None
        assert recipe.id == test_recipe.id
        assert recipe.title == test_recipe.title

    def test_get_recipe_not_found(self, db):
        """Test getting non-existent recipe"""
        recipe = RecipeService.get_recipe(db, uuid4())

        assert recipe is None

    def test_get_recipe_deleted(self, db, test_recipe):
        """Test getting deleted recipe"""
        test_recipe.is_deleted = True
        db.commit()

        recipe = RecipeService.get_recipe(db, test_recipe.id)

        assert recipe is None

    def test_get_recipe_specific_version(self, db, test_recipe, test_user):
        """Test getting specific version of recipe"""
        # Create version 2
        recipe_data = RecipeUpdate(
            title="Updated Recipe",
            description="Updated",
            prep_time_minutes=20,
            cook_time_minutes=40,
            servings=6,
            difficulty="hard",
            instructions="New instructions",
            ingredients=[],
            tags=[],
        )
        RecipeService.update_recipe(db, test_recipe.id, recipe_data, test_user.id)

        # Get version 1
        recipe = RecipeService.get_recipe(db, test_recipe.id, version=1)

        assert recipe is not None
        assert recipe.current_version == 2  # But we requested version 1

    def test_list_recipes_default(self, db, test_user, test_recipes):
        """Test listing recipes with default parameters"""
        recipes, total = RecipeService.list_recipes(db, test_user.id)

        assert total == 5
        assert len(recipes) == 5

    def test_list_recipes_pagination(self, db, test_user, test_recipes):
        """Test recipe pagination"""
        recipes, total = RecipeService.list_recipes(db, test_user.id, page=1, limit=2)

        assert total == 5
        assert len(recipes) == 2

        recipes, total = RecipeService.list_recipes(db, test_user.id, page=2, limit=2)

        assert total == 5
        assert len(recipes) == 2

    def test_list_recipes_search(self, db, test_user, test_recipes):
        """Test recipe search"""
        recipes, total = RecipeService.list_recipes(db, test_user.id, search="pasta")

        assert total == 1
        assert recipes[0].title == "Pasta Carbonara"

    def test_list_recipes_search_case_insensitive(self, db, test_user, test_recipes):
        """Test case-insensitive search"""
        recipes, total = RecipeService.list_recipes(db, test_user.id, search="PASTA")

        assert total == 1

    def test_list_recipes_filter_difficulty(self, db, test_user, test_recipes):
        """Test filtering by difficulty"""
        recipes, total = RecipeService.list_recipes(db, test_user.id, difficulty="easy")

        assert total == 2
        for recipe in recipes:
            version = (
                db.query(RecipeVersion)
                .filter(
                    RecipeVersion.recipe_id == recipe.id,
                    RecipeVersion.version_number == recipe.current_version,
                )
                .first()
            )
            assert version.difficulty == "easy"

    def test_list_recipes_filter_never_tried(self, db, test_user, test_recipes):
        """Test filtering never tried recipes"""
        # Mark one as cooked
        test_recipes[0].times_cooked = 1
        db.commit()

        recipes, total = RecipeService.list_recipes(
            db, test_user.id, filter_type="never_tried"
        )

        assert total == 4

    def test_list_recipes_filter_not_recent(self, db, test_user, test_recipes):
        """Test filtering not recently cooked recipes"""
        # Mark one as cooked recently
        test_recipes[0].last_cooked_date = date.today()
        test_recipes[1].last_cooked_date = date.today() - timedelta(days=20)
        db.commit()

        recipes, total = RecipeService.list_recipes(
            db, test_user.id, filter_type="not_recent"
        )

        # Should exclude the one cooked today (default rotation is 14 days)
        assert total == 4

    def test_update_recipe_creates_new_version(self, db, test_recipe, test_user):
        """Test that updating recipe creates new version"""
        original_version = test_recipe.current_version

        recipe_data = RecipeUpdate(
            title="Updated Title",
            description="Updated description",
            prep_time_minutes=25,
            cook_time_minutes=35,
            servings=6,
            difficulty="hard",
            instructions="Updated instructions",
            change_description="Major update",
            ingredients=[
                IngredientInput(
                    name="new_ingredient", quantity=150, unit="g", category="other"
                )
            ],
            tags=["new_tag"],
        )

        updated = RecipeService.update_recipe(
            db, test_recipe.id, recipe_data, test_user.id
        )

        assert updated.current_version == original_version + 1
        assert updated.title == "Updated Title"

        # Check new version exists
        new_version = (
            db.query(RecipeVersion)
            .filter(
                RecipeVersion.recipe_id == test_recipe.id,
                RecipeVersion.version_number == original_version + 1,
            )
            .first()
        )
        assert new_version is not None
        assert new_version.change_description == "Major update"

    def test_update_recipe_not_found(self, db, test_user):
        """Test updating non-existent recipe"""
        recipe_data = RecipeUpdate(
            title="Updated",
            description="Updated",
            prep_time_minutes=10,
            cook_time_minutes=20,
            servings=4,
            difficulty="easy",
            instructions="Instructions",
            ingredients=[],
            tags=[],
        )

        updated = RecipeService.update_recipe(db, uuid4(), recipe_data, test_user.id)

        assert updated is None

    def test_delete_recipe_soft_delete(self, db, test_recipe):
        """Test soft delete of recipe"""
        result = RecipeService.delete_recipe(db, test_recipe.id)

        assert result is True

        # Recipe should still exist but be marked deleted
        recipe = db.query(Recipe).filter(Recipe.id == test_recipe.id).first()
        assert recipe is not None
        assert recipe.is_deleted is True

    def test_delete_recipe_not_found(self, db):
        """Test deleting non-existent recipe"""
        result = RecipeService.delete_recipe(db, uuid4())

        assert result is False

    def test_get_recipe_versions(self, db, test_recipe, test_user):
        """Test getting all versions of a recipe"""
        # Create additional versions
        for i in range(2):
            recipe_data = RecipeUpdate(
                title=f"Version {i+2}",
                description="Updated",
                prep_time_minutes=10,
                cook_time_minutes=20,
                servings=4,
                difficulty="easy",
                instructions="Instructions",
                ingredients=[],
                tags=[],
            )
            RecipeService.update_recipe(db, test_recipe.id, recipe_data, test_user.id)

        versions = RecipeService.get_recipe_versions(db, test_recipe.id)

        assert len(versions) == 3
        # Should be in descending order
        assert versions[0].version_number == 3
        assert versions[1].version_number == 2
        assert versions[2].version_number == 1

    def test_revert_recipe_to_previous_version(self, db, test_recipe, test_user):
        """Test reverting recipe to previous version"""
        # Create version 2
        recipe_data = RecipeUpdate(
            title="Version 2",
            description="Updated",
            prep_time_minutes=99,
            cook_time_minutes=99,
            servings=10,
            difficulty="hard",
            instructions="Bad instructions",
            ingredients=[],
            tags=[],
        )
        RecipeService.update_recipe(db, test_recipe.id, recipe_data, test_user.id)

        # Revert to version 1
        reverted = RecipeService.revert_recipe(db, test_recipe.id, 1, test_user.id)

        assert reverted is not None
        assert reverted.current_version == 3  # Creates new version as copy

        # Check version 3 has same data as version 1
        version3 = (
            db.query(RecipeVersion)
            .filter(
                RecipeVersion.recipe_id == test_recipe.id,
                RecipeVersion.version_number == 3,
            )
            .first()
        )
        version1 = (
            db.query(RecipeVersion)
            .filter(
                RecipeVersion.recipe_id == test_recipe.id,
                RecipeVersion.version_number == 1,
            )
            .first()
        )

        assert version3.prep_time_minutes == version1.prep_time_minutes
        assert version3.cook_time_minutes == version1.cook_time_minutes
        assert version3.change_description == "Reverted to version 1"

    def test_revert_recipe_not_found(self, db, test_user):
        """Test reverting non-existent recipe"""
        reverted = RecipeService.revert_recipe(db, uuid4(), 1, test_user.id)

        assert reverted is None

    def test_revert_recipe_invalid_version(self, db, test_recipe, test_user):
        """Test reverting to non-existent version"""
        reverted = RecipeService.revert_recipe(db, test_recipe.id, 999, test_user.id)

        assert reverted is None

    def test_recipe_tracking_times_cooked(self, db, test_recipe):
        """Test that times_cooked is tracked correctly"""
        assert test_recipe.times_cooked == 0

        test_recipe.times_cooked = 5
        db.commit()

        recipe = RecipeService.get_recipe(db, test_recipe.id)
        assert recipe.times_cooked == 5

    def test_recipe_tracking_last_cooked_date(self, db, test_recipe):
        """Test that last_cooked_date is tracked correctly"""
        assert test_recipe.last_cooked_date is None

        test_date = date.today() - timedelta(days=5)
        test_recipe.last_cooked_date = test_date
        db.commit()

        recipe = RecipeService.get_recipe(db, test_recipe.id)
        assert recipe.last_cooked_date == test_date

"""
Unit Tests for Rating Service
Tests rating CRUD operations and favorites calculation
"""

from uuid import uuid4

import pytest

from src.models.rating import Rating
from src.schemas.rating import RatingCreate
from src.services.rating_service import RatingService


@pytest.mark.unit
class TestRatingService:
    """Test cases for rating service"""

    def test_create_rating_success(self, db, test_recipe, test_user):
        """Test successful rating creation"""
        rating_data = RatingCreate(
            rating=True, feedback="Excellent recipe!", modifications="Added more salt"
        )

        rating = RatingService.create_or_update_rating(
            db, test_recipe.id, test_user.id, rating_data
        )

        assert rating.id is not None
        assert rating.recipe_id == test_recipe.id
        assert rating.user_id == test_user.id
        assert rating.rating is True
        assert rating.feedback == "Excellent recipe!"

    def test_create_rating_thumbs_down(self, db, test_recipe, test_user):
        """Test creating thumbs down rating"""
        rating_data = RatingCreate(rating=False, feedback="Not my favorite")

        rating = RatingService.create_or_update_rating(
            db, test_recipe.id, test_user.id, rating_data
        )

        assert rating.rating is False

    def test_update_existing_rating(self, db, test_recipe, test_user):
        """Test updating existing rating"""
        # Create initial rating
        rating_data = RatingCreate(rating=True, feedback="Good")
        initial = RatingService.create_or_update_rating(
            db, test_recipe.id, test_user.id, rating_data
        )

        # Update rating
        rating_data = RatingCreate(rating=False, feedback="Changed my mind")
        updated = RatingService.create_or_update_rating(
            db, test_recipe.id, test_user.id, rating_data
        )

        assert updated.id == initial.id
        assert updated.rating is False
        assert updated.feedback == "Changed my mind"

        # Should still be only one rating
        count = (
            db.query(Rating)
            .filter(Rating.recipe_id == test_recipe.id, Rating.user_id == test_user.id)
            .count()
        )
        assert count == 1

    def test_get_rating_by_id(self, db, test_rating):
        """Test getting rating by ID"""
        rating = RatingService.get_rating(db, test_rating.id)

        assert rating is not None
        assert rating.id == test_rating.id

    def test_get_rating_not_found(self, db):
        """Test getting non-existent rating"""
        rating = RatingService.get_rating(db, uuid4())

        assert rating is None

    def test_get_recipe_ratings(self, db, test_recipe, test_user):
        """Test getting all ratings for a recipe"""
        # Create multiple ratings
        rating_data = RatingCreate(rating=True)
        RatingService.create_or_update_rating(
            db, test_recipe.id, test_user.id, rating_data
        )

        ratings = RatingService.get_recipe_ratings(db, test_recipe.id)

        assert len(ratings) >= 1

    def test_get_rating_summary_with_ratings(
        self, db, test_recipe, test_user, admin_user
    ):
        """Test rating summary calculation"""
        # Create ratings
        RatingService.create_or_update_rating(
            db, test_recipe.id, test_user.id, RatingCreate(rating=True)
        )
        RatingService.create_or_update_rating(
            db, test_recipe.id, admin_user.id, RatingCreate(rating=True)
        )

        summary = RatingService.get_rating_summary(db, test_recipe.id)

        assert summary["recipe_id"] == test_recipe.id
        assert summary["thumbs_up_count"] == 2
        assert summary["thumbs_down_count"] == 0
        assert summary["total_ratings"] == 2

    def test_get_rating_summary_empty(self, db, test_recipe):
        """Test rating summary with no ratings"""
        summary = RatingService.get_rating_summary(db, test_recipe.id)

        assert summary["thumbs_up_count"] == 0
        assert summary["thumbs_down_count"] == 0
        assert summary["total_ratings"] == 0
        assert summary["is_favorite"] is False

    def test_favorites_calculation_meets_threshold(self, db, test_recipe):
        """Test that recipe becomes favorite when meeting threshold"""
        # Create test users and ratings (need at least 3 raters for default)
        from src.core.security import SecurityManager
        from src.models.user import User

        users = []
        for i in range(4):
            user = User(
                username=f"user{i}",
                email=f"user{i}@test.com",
                password_hash=SecurityManager.hash_password("pass"),
                role="user",
            )
            db.add(user)
            users.append(user)

        db.commit()

        # Add 4 thumbs up (100% positive)
        for user in users:
            RatingService.create_or_update_rating(
                db, test_recipe.id, user.id, RatingCreate(rating=True)
            )

        summary = RatingService.get_rating_summary(db, test_recipe.id)

        assert summary["is_favorite"] is True

    def test_favorites_calculation_below_threshold(self, db, test_recipe):
        """Test that recipe is not favorite below threshold"""
        from src.core.security import SecurityManager
        from src.models.user import User

        users = []
        for i in range(4):
            user = User(
                username=f"user{i}",
                email=f"user{i}@test.com",
                password_hash=SecurityManager.hash_password("pass"),
                role="user",
            )
            db.add(user)
            users.append(user)

        db.commit()

        # Add 2 thumbs up, 2 thumbs down (50% - below 75% threshold)
        for i, user in enumerate(users):
            RatingService.create_or_update_rating(
                db,
                test_recipe.id,
                user.id,
                RatingCreate(rating=True if i < 2 else False),
            )

        summary = RatingService.get_rating_summary(db, test_recipe.id)

        assert summary["is_favorite"] is False

    def test_favorites_requires_minimum_raters(self, db, test_recipe, test_user):
        """Test that favorites requires minimum number of raters"""
        # Only 1 rater with thumbs up (below minimum of 3)
        RatingService.create_or_update_rating(
            db, test_recipe.id, test_user.id, RatingCreate(rating=True)
        )

        summary = RatingService.get_rating_summary(db, test_recipe.id)

        assert summary["is_favorite"] is False

    def test_update_rating_by_id(self, db, test_rating, test_user):
        """Test updating rating by ID"""
        rating_data = RatingCreate(rating=False, feedback="Updated feedback")

        updated = RatingService.update_rating(
            db, test_rating.id, test_user.id, rating_data
        )

        assert updated is not None
        assert updated.rating is False
        assert updated.feedback == "Updated feedback"

    def test_update_rating_unauthorized(self, db, test_rating, admin_user):
        """Test that user cannot update another user's rating"""
        rating_data = RatingCreate(rating=False)

        updated = RatingService.update_rating(
            db, test_rating.id, admin_user.id, rating_data
        )

        assert updated is None

    def test_delete_rating_success(self, db, test_rating, test_user):
        """Test successful rating deletion"""
        result = RatingService.delete_rating(db, test_rating.id, test_user.id)

        assert result is True

        # Rating should be deleted
        rating = db.query(Rating).filter(Rating.id == test_rating.id).first()
        assert rating is None

    def test_delete_rating_unauthorized(self, db, test_rating, admin_user):
        """Test that user cannot delete another user's rating"""
        result = RatingService.delete_rating(db, test_rating.id, admin_user.id)

        assert result is False

        # Rating should still exist
        rating = db.query(Rating).filter(Rating.id == test_rating.id).first()
        assert rating is not None

    def test_delete_rating_not_found(self, db, test_user):
        """Test deleting non-existent rating"""
        result = RatingService.delete_rating(db, uuid4(), test_user.id)

        assert result is False

    def test_get_user_rating(self, db, test_recipe, test_user):
        """Test getting specific user's rating"""
        rating_data = RatingCreate(rating=True)
        RatingService.create_or_update_rating(
            db, test_recipe.id, test_user.id, rating_data
        )

        rating = RatingService.get_user_rating(db, test_recipe.id, test_user.id)

        assert rating is not None
        assert rating.user_id == test_user.id

    def test_get_user_rating_not_found(self, db, test_recipe, test_user):
        """Test getting non-existent user rating"""
        rating = RatingService.get_user_rating(db, test_recipe.id, test_user.id)

        assert rating is None

    def test_is_favorite(self, db, test_recipe):
        """Test is_favorite helper method"""
        from src.core.security import SecurityManager
        from src.models.user import User

        # Create users and give thumbs up
        users = []
        for i in range(3):
            user = User(
                username=f"fav_user{i}",
                email=f"fav{i}@test.com",
                password_hash=SecurityManager.hash_password("pass"),
                role="user",
            )
            db.add(user)
            users.append(user)

        db.commit()

        for user in users:
            RatingService.create_or_update_rating(
                db, test_recipe.id, user.id, RatingCreate(rating=True)
            )

        is_fav = RatingService.is_favorite(db, test_recipe.id)

        assert is_fav is True

"""
Rating Service
Business logic for recipe ratings and favorites calculation
"""

import logging
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.app_settings import AppSettings
from src.models.rating import Rating
from src.models.recipe import Recipe
from src.schemas.rating import RatingCreate

logger = logging.getLogger(__name__)


class RatingService:
    """Service for recipe ratings"""

    @staticmethod
    def create_or_update_rating(
        db: Session, recipe_id: UUID, user_id: UUID, rating_data: RatingCreate
    ) -> Rating:
        """Create or update rating for recipe"""
        # Check if rating already exists
        existing = (
            db.query(Rating)
            .filter(Rating.recipe_id == recipe_id, Rating.user_id == user_id)
            .first()
        )

        if existing:
            # Update existing rating
            existing.rating = rating_data.rating
            existing.feedback = rating_data.feedback
            existing.modifications = rating_data.modifications
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new rating
            rating = Rating(
                recipe_id=recipe_id,
                user_id=user_id,
                rating=rating_data.rating,
                feedback=rating_data.feedback,
                modifications=rating_data.modifications,
            )
            db.add(rating)
            db.commit()
            db.refresh(rating)
            return rating

    @staticmethod
    def get_rating(db: Session, rating_id: UUID) -> Optional[Rating]:
        """Get rating by ID"""
        return db.query(Rating).filter(Rating.id == rating_id).first()

    @staticmethod
    def get_recipe_ratings(db: Session, recipe_id: UUID) -> List[Rating]:
        """Get all ratings for a recipe"""
        return db.query(Rating).filter(Rating.recipe_id == recipe_id).all()

    @staticmethod
    def get_rating_summary(db: Session, recipe_id: UUID) -> Dict:
        """
        Get rating summary for recipe including favorite status.

        Returns:
            Dict with thumbs_up_count, thumbs_down_count, total_ratings, is_favorite
        """
        ratings = db.query(Rating).filter(Rating.recipe_id == recipe_id).all()

        thumbs_up = sum(1 for r in ratings if r.rating)
        thumbs_down = sum(1 for r in ratings if not r.rating)
        total = len(ratings)

        # Get app settings for favorites threshold
        settings = db.query(AppSettings).first()
        threshold = float(settings.favorites_threshold) if settings else 0.75
        min_raters = settings.favorites_min_raters if settings else 3

        # Calculate favorite status
        is_favorite = False
        if total >= min_raters:
            percentage = thumbs_up / total if total > 0 else 0
            is_favorite = percentage >= threshold

        return {
            "recipe_id": recipe_id,
            "thumbs_up_count": thumbs_up,
            "thumbs_down_count": thumbs_down,
            "total_ratings": total,
            "is_favorite": is_favorite,
        }

    @staticmethod
    def update_rating(
        db: Session, rating_id: UUID, user_id: UUID, rating_data: RatingCreate
    ) -> Optional[Rating]:
        """Update existing rating"""
        rating = (
            db.query(Rating)
            .filter(
                Rating.id == rating_id,
                Rating.user_id == user_id,  # Ensure user owns the rating
            )
            .first()
        )

        if not rating:
            return None

        rating.rating = rating_data.rating
        rating.feedback = rating_data.feedback
        rating.modifications = rating_data.modifications

        db.commit()
        db.refresh(rating)
        return rating

    @staticmethod
    def delete_rating(db: Session, rating_id: UUID, user_id: UUID) -> bool:
        """Delete rating (user must own it)"""
        rating = (
            db.query(Rating)
            .filter(Rating.id == rating_id, Rating.user_id == user_id)
            .first()
        )

        if not rating:
            return False

        db.delete(rating)
        db.commit()
        return True

    @staticmethod
    def get_user_rating(
        db: Session, recipe_id: UUID, user_id: UUID
    ) -> Optional[Rating]:
        """Get specific user's rating for a recipe"""
        return (
            db.query(Rating)
            .filter(Rating.recipe_id == recipe_id, Rating.user_id == user_id)
            .first()
        )

    @staticmethod
    def is_favorite(db: Session, recipe_id: UUID) -> bool:
        """Check if recipe is a favorite"""
        summary = RatingService.get_rating_summary(db, recipe_id)
        return summary["is_favorite"]

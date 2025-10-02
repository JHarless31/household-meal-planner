"""
Recipe Suggestion Service
Smart algorithms for suggesting recipes based on various strategies
"""

import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from src.models.inventory import InventoryItem
from src.models.menu_plan import PlannedMeal
from src.models.rating import Rating
from src.models.recipe import Ingredient, Recipe, RecipeTag, RecipeVersion

logger = logging.getLogger(__name__)


class RecipeSuggestionService:
    """Service for intelligent recipe suggestions"""

    @staticmethod
    def suggest_by_rotation(
        db: Session, user_id: UUID, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Suggest recipes based on rotation (not cooked recently).

        Prioritizes:
        1. Recipes never cooked (times_cooked = 0)
        2. Recipes not cooked in longest time
        3. Recipes cooked least frequently

        Args:
            db: Database session
            user_id: User requesting suggestions
            limit: Number of suggestions to return

        Returns:
            List of recipe suggestions with metadata
        """
        # Get recipes sorted by rotation priority
        recipes = (
            db.query(Recipe)
            .filter(Recipe.is_deleted == False)
            .order_by(
                # Never cooked recipes first (NULL last_cooked_date)
                Recipe.last_cooked_date.asc().nulls_first(),
                # Then by times cooked (least cooked first)
                Recipe.times_cooked.asc(),
                # Finally by title for consistent ordering
                Recipe.title.asc(),
            )
            .limit(limit)
            .all()
        )

        suggestions = []
        for recipe in recipes:
            # Calculate days since last cooked
            days_since_cooked = None
            if recipe.last_cooked_date:
                days_since_cooked = (date.today() - recipe.last_cooked_date).days

            # Generate reason
            if recipe.times_cooked == 0:
                reason = "Never tried before"
            elif days_since_cooked:
                reason = f"Not cooked in {days_since_cooked} days"
            else:
                reason = "Due for rotation"

            suggestions.append(
                {
                    "recipe_id": str(recipe.id),
                    "title": recipe.title,
                    "description": recipe.description,
                    "times_cooked": recipe.times_cooked,
                    "last_cooked_date": (
                        recipe.last_cooked_date.isoformat()
                        if recipe.last_cooked_date
                        else None
                    ),
                    "days_since_cooked": days_since_cooked,
                    "reason": reason,
                    "strategy": "rotation",
                }
            )

        return suggestions

    @staticmethod
    def suggest_by_favorites(
        db: Session, user_id: UUID, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Suggest household favorite recipes based on ratings.

        Prioritizes recipes with:
        1. Highest average rating
        2. Most number of ratings (popularity)

        Args:
            db: Database session
            user_id: User requesting suggestions
            limit: Number of suggestions to return

        Returns:
            List of favorite recipe suggestions
        """
        # Query recipes with average rating and rating count
        recipes_with_ratings = (
            db.query(
                Recipe,
                func.avg(Rating.rating).label("avg_rating"),
                func.count(Rating.id).label("rating_count"),
            )
            .join(Rating, Recipe.id == Rating.recipe_id)
            .filter(Recipe.is_deleted == False)
            .group_by(Recipe.id)
            .order_by(func.avg(Rating.rating).desc(), func.count(Rating.id).desc())
            .limit(limit)
            .all()
        )

        suggestions = []
        for recipe, avg_rating, rating_count in recipes_with_ratings:
            suggestions.append(
                {
                    "recipe_id": str(recipe.id),
                    "title": recipe.title,
                    "description": recipe.description,
                    "average_rating": float(avg_rating) if avg_rating else 0,
                    "rating_count": rating_count,
                    "reason": f"Household favorite ({avg_rating:.1f}★ from {rating_count} ratings)",
                    "strategy": "favorites",
                }
            )

        return suggestions

    @staticmethod
    def suggest_never_tried(
        db: Session, user_id: UUID, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Suggest recipes that have never been cooked.

        Args:
            db: Database session
            user_id: User requesting suggestions
            limit: Number of suggestions to return

        Returns:
            List of never-tried recipe suggestions
        """
        recipes = (
            db.query(Recipe)
            .filter(Recipe.is_deleted == False, Recipe.times_cooked == 0)
            .order_by(Recipe.created_at.desc())  # Newest recipes first
            .limit(limit)
            .all()
        )

        suggestions = []
        for recipe in recipes:
            suggestions.append(
                {
                    "recipe_id": str(recipe.id),
                    "title": recipe.title,
                    "description": recipe.description,
                    "times_cooked": 0,
                    "reason": "Never tried - give it a try!",
                    "strategy": "never_tried",
                }
            )

        return suggestions

    @staticmethod
    def suggest_by_available_inventory(
        db: Session,
        user_id: UUID,
        limit: int = 10,
        min_ingredient_match_percent: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """
        Suggest recipes based on available inventory items.

        Matches recipe ingredients against current inventory and suggests
        recipes where most ingredients are available.

        Args:
            db: Database session
            user_id: User requesting suggestions
            limit: Number of suggestions to return
            min_ingredient_match_percent: Minimum % of ingredients that must be available

        Returns:
            List of suggestions based on inventory availability
        """
        # Get all active recipes with their current versions
        recipes = db.query(Recipe).filter(Recipe.is_deleted == False).all()

        # Get current inventory items
        inventory_items = (
            db.query(InventoryItem).filter(InventoryItem.quantity > 0).all()
        )

        # Create set of available ingredient names (case-insensitive)
        available_ingredients = {
            item.item_name.lower().strip() for item in inventory_items
        }

        suggestions = []

        for recipe in recipes:
            # Get current version ingredients
            version = (
                db.query(RecipeVersion)
                .filter(
                    RecipeVersion.recipe_id == recipe.id,
                    RecipeVersion.version_number == recipe.current_version,
                )
                .first()
            )

            if not version:
                continue

            # Get non-optional ingredients
            ingredients = (
                db.query(Ingredient)
                .filter(
                    Ingredient.recipe_version_id == version.id,
                    Ingredient.is_optional == False,
                )
                .all()
            )

            if not ingredients:
                continue

            # Calculate match percentage
            total_ingredients = len(ingredients)
            matched_ingredients = 0
            missing_ingredients = []

            for ing in ingredients:
                ing_name = ing.name.lower().strip()
                if ing_name in available_ingredients:
                    matched_ingredients += 1
                else:
                    missing_ingredients.append(ing.name)

            match_percent = (
                matched_ingredients / total_ingredients if total_ingredients > 0 else 0
            )

            # Only suggest if match percentage is above threshold
            if match_percent >= min_ingredient_match_percent:
                suggestions.append(
                    {
                        "recipe_id": str(recipe.id),
                        "title": recipe.title,
                        "description": recipe.description,
                        "match_percent": round(match_percent * 100, 1),
                        "matched_ingredients": matched_ingredients,
                        "total_ingredients": total_ingredients,
                        "missing_ingredients": missing_ingredients[
                            :3
                        ],  # First 3 missing
                        "reason": f"{match_percent*100:.0f}% ingredients available",
                        "strategy": "available_inventory",
                    }
                )

        # Sort by match percentage (highest first) and limit
        suggestions.sort(key=lambda x: x["match_percent"], reverse=True)
        return suggestions[:limit]

    @staticmethod
    def suggest_seasonal(
        db: Session, user_id: UUID, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Suggest recipes based on current season.

        Uses recipe tags to identify seasonal recipes.
        Seasons: spring, summer, fall, winter

        Args:
            db: Database session
            user_id: User requesting suggestions
            limit: Number of suggestions to return

        Returns:
            List of seasonal recipe suggestions
        """
        # Determine current season based on month
        current_month = datetime.now().month
        if current_month in [3, 4, 5]:
            season = "spring"
        elif current_month in [6, 7, 8]:
            season = "summer"
        elif current_month in [9, 10, 11]:
            season = "fall"
        else:
            season = "winter"

        # Find recipes with seasonal tags
        recipes = (
            db.query(Recipe)
            .join(RecipeTag, Recipe.id == RecipeTag.recipe_id)
            .filter(Recipe.is_deleted == False, RecipeTag.tag.ilike(f"%{season}%"))
            .limit(limit)
            .all()
        )

        suggestions = []
        for recipe in recipes:
            suggestions.append(
                {
                    "recipe_id": str(recipe.id),
                    "title": recipe.title,
                    "description": recipe.description,
                    "reason": f"Perfect for {season}!",
                    "season": season,
                    "strategy": "seasonal",
                }
            )

        return suggestions

    @staticmethod
    def suggest_quick_meals(
        db: Session, user_id: UUID, limit: int = 10, max_total_time: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Suggest quick recipes that can be prepared in limited time.

        Args:
            db: Database session
            user_id: User requesting suggestions
            limit: Number of suggestions to return
            max_total_time: Maximum total time (prep + cook) in minutes

        Returns:
            List of quick meal suggestions
        """
        # Find recipes with their current version
        recipes = db.query(Recipe).filter(Recipe.is_deleted == False).all()

        suggestions = []

        for recipe in recipes:
            version = (
                db.query(RecipeVersion)
                .filter(
                    RecipeVersion.recipe_id == recipe.id,
                    RecipeVersion.version_number == recipe.current_version,
                )
                .first()
            )

            if not version:
                continue

            # Calculate total time
            prep_time = version.prep_time_minutes or 0
            cook_time = version.cook_time_minutes or 0
            total_time = prep_time + cook_time

            if total_time > 0 and total_time <= max_total_time:
                suggestions.append(
                    {
                        "recipe_id": str(recipe.id),
                        "title": recipe.title,
                        "description": recipe.description,
                        "prep_time_minutes": prep_time,
                        "cook_time_minutes": cook_time,
                        "total_time_minutes": total_time,
                        "reason": f"Ready in {total_time} minutes",
                        "strategy": "quick_meals",
                    }
                )

        # Sort by total time (fastest first)
        suggestions.sort(key=lambda x: x["total_time_minutes"])
        return suggestions[:limit]

    @staticmethod
    def get_suggestions(
        db: Session, user_id: UUID, strategy: str = "rotation", limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recipe suggestions based on specified strategy.

        Args:
            db: Database session
            user_id: User requesting suggestions
            strategy: Strategy to use (rotation, favorites, never_tried, available_inventory, seasonal, quick_meals)
            limit: Number of suggestions to return

        Returns:
            List of recipe suggestions
        """
        strategy_map = {
            "rotation": RecipeSuggestionService.suggest_by_rotation,
            "favorites": RecipeSuggestionService.suggest_by_favorites,
            "never_tried": RecipeSuggestionService.suggest_never_tried,
            "available_inventory": RecipeSuggestionService.suggest_by_available_inventory,
            "seasonal": RecipeSuggestionService.suggest_seasonal,
            "quick_meals": RecipeSuggestionService.suggest_quick_meals,
        }

        suggestion_func = strategy_map.get(strategy)
        if not suggestion_func:
            logger.warning(f"Unknown strategy: {strategy}, defaulting to rotation")
            suggestion_func = RecipeSuggestionService.suggest_by_rotation

        return suggestion_func(db, user_id, limit)

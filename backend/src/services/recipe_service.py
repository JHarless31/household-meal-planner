"""
Recipe Service
Business logic for recipe operations including versioning
"""

from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta, date
from uuid import UUID
import logging

from src.models.recipe import Recipe, RecipeVersion, Ingredient, RecipeTag, RecipeImage
from src.models.rating import Rating
from src.models.inventory import InventoryItem
from src.models.app_settings import AppSettings
from src.schemas.recipe import (
    RecipeCreate, RecipeUpdate, RecipeSummary, RecipeResponse,
    IngredientInput, IngredientResponse, RecipeVersionResponse
)

logger = logging.getLogger(__name__)


class RecipeService:
    """Service for recipe management"""

    @staticmethod
    def create_recipe(
        db: Session,
        recipe_data: RecipeCreate,
        user_id: UUID
    ) -> Recipe:
        """
        Create a new recipe with version 1.

        Args:
            db: Database session
            recipe_data: Recipe creation data
            user_id: User creating the recipe

        Returns:
            Recipe: Created recipe
        """
        # Create recipe
        recipe = Recipe(
            title=recipe_data.title,
            description=recipe_data.description,
            source_url=recipe_data.source_url,
            source_type="scraped" if recipe_data.source_url else "manual",
            created_by=user_id,
            current_version=1
        )
        db.add(recipe)
        db.flush()

        # Create version 1
        version = RecipeVersion(
            recipe_id=recipe.id,
            version_number=1,
            prep_time_minutes=recipe_data.prep_time_minutes,
            cook_time_minutes=recipe_data.cook_time_minutes,
            servings=recipe_data.servings,
            difficulty=recipe_data.difficulty,
            instructions=recipe_data.instructions,
            modified_by=user_id
        )
        db.add(version)
        db.flush()

        # Add ingredients
        for idx, ing_data in enumerate(recipe_data.ingredients):
            ingredient = Ingredient(
                recipe_version_id=version.id,
                name=ing_data.name,
                quantity=ing_data.quantity,
                unit=ing_data.unit,
                category=ing_data.category,
                is_optional=ing_data.is_optional or False,
                display_order=idx
            )
            db.add(ingredient)

        # Add tags
        if recipe_data.tags:
            for tag in recipe_data.tags:
                recipe_tag = RecipeTag(recipe_id=recipe.id, tag=tag.lower())
                db.add(recipe_tag)

        db.commit()
        db.refresh(recipe)
        return recipe

    @staticmethod
    def get_recipe(db: Session, recipe_id: UUID, version: Optional[int] = None) -> Optional[Recipe]:
        """
        Get recipe by ID, optionally at specific version.

        Args:
            db: Database session
            recipe_id: Recipe ID
            version: Optional version number (defaults to current)

        Returns:
            Optional[Recipe]: Recipe or None if not found
        """
        recipe = db.query(Recipe).filter(
            Recipe.id == recipe_id,
            Recipe.is_deleted == False
        ).first()

        if not recipe:
            return None

        # If version specified, load that version's data
        if version is not None:
            recipe_version = db.query(RecipeVersion).filter(
                RecipeVersion.recipe_id == recipe_id,
                RecipeVersion.version_number == version
            ).first()

            if not recipe_version:
                return None

        return recipe

    @staticmethod
    def list_recipes(
        db: Session,
        user_id: UUID,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        difficulty: Optional[str] = None,
        filter_type: Optional[str] = None
    ) -> Tuple[List[Recipe], int]:
        """
        List recipes with filters and pagination.

        Args:
            db: Database session
            user_id: Current user ID
            page: Page number (1-indexed)
            limit: Items per page
            search: Search query
            tags: Filter by tags
            difficulty: Filter by difficulty
            filter_type: Special filter (favorites, not_recent, never_tried, available_inventory)

        Returns:
            Tuple[List[Recipe], int]: List of recipes and total count
        """
        query = db.query(Recipe).filter(Recipe.is_deleted == False)

        # Search
        if search:
            query = query.filter(
                or_(
                    Recipe.title.ilike(f'%{search}%'),
                    Recipe.description.ilike(f'%{search}%')
                )
            )

        # Tags filter
        if tags:
            for tag in tags:
                query = query.join(RecipeTag).filter(RecipeTag.tag == tag.lower())

        # Difficulty filter (join with current version)
        if difficulty:
            query = query.join(RecipeVersion).filter(
                RecipeVersion.version_number == Recipe.current_version,
                RecipeVersion.difficulty == difficulty
            )

        # Special filters
        if filter_type == "favorites":
            # Get app settings for favorites threshold
            settings = db.query(AppSettings).first()
            threshold = float(settings.favorites_threshold) if settings else 0.75
            min_raters = settings.favorites_min_raters if settings else 3

            # Subquery for favorites
            favorites_subq = db.query(
                Rating.recipe_id
            ).group_by(
                Rating.recipe_id
            ).having(
                and_(
                    func.count(Rating.id) >= min_raters,
                    func.sum(func.cast(Rating.rating, db.dialect.Integer)) / func.count(Rating.id) >= threshold
                )
            ).subquery()

            query = query.filter(Recipe.id.in_(favorites_subq))

        elif filter_type == "not_recent":
            # Get rotation period from settings
            settings = db.query(AppSettings).first()
            days = settings.rotation_period_days if settings else 14

            cutoff_date = date.today() - timedelta(days=days)
            query = query.filter(
                or_(
                    Recipe.last_cooked_date == None,
                    Recipe.last_cooked_date <= cutoff_date
                )
            )

        elif filter_type == "never_tried":
            query = query.filter(Recipe.times_cooked == 0)

        elif filter_type == "available_inventory":
            # This is complex - check if all ingredients are in stock
            # For simplicity, we'll just return all recipes
            # In production, you'd join with inventory and check quantities
            pass

        # Count total
        total = query.count()

        # Paginate
        query = query.offset((page - 1) * limit).limit(limit)

        recipes = query.all()
        return recipes, total

    @staticmethod
    def update_recipe(
        db: Session,
        recipe_id: UUID,
        recipe_data: RecipeUpdate,
        user_id: UUID
    ) -> Optional[Recipe]:
        """
        Update recipe by creating a new version.

        Args:
            db: Database session
            recipe_id: Recipe to update
            recipe_data: Update data
            user_id: User making the update

        Returns:
            Optional[Recipe]: Updated recipe or None if not found
        """
        recipe = db.query(Recipe).filter(
            Recipe.id == recipe_id,
            Recipe.is_deleted == False
        ).first()

        if not recipe:
            return None

        # Create new version
        new_version_number = recipe.current_version + 1

        version = RecipeVersion(
            recipe_id=recipe.id,
            version_number=new_version_number,
            prep_time_minutes=recipe_data.prep_time_minutes,
            cook_time_minutes=recipe_data.cook_time_minutes,
            servings=recipe_data.servings,
            difficulty=recipe_data.difficulty,
            instructions=recipe_data.instructions,
            change_description=recipe_data.change_description,
            modified_by=user_id
        )
        db.add(version)
        db.flush()

        # Add ingredients for new version
        for idx, ing_data in enumerate(recipe_data.ingredients):
            ingredient = Ingredient(
                recipe_version_id=version.id,
                name=ing_data.name,
                quantity=ing_data.quantity,
                unit=ing_data.unit,
                category=ing_data.category,
                is_optional=ing_data.is_optional or False,
                display_order=idx
            )
            db.add(ingredient)

        # Update recipe metadata
        recipe.title = recipe_data.title
        recipe.description = recipe_data.description
        recipe.current_version = new_version_number

        # Update tags (remove old, add new)
        db.query(RecipeTag).filter(RecipeTag.recipe_id == recipe.id).delete()
        if recipe_data.tags:
            for tag in recipe_data.tags:
                recipe_tag = RecipeTag(recipe_id=recipe.id, tag=tag.lower())
                db.add(recipe_tag)

        db.commit()
        db.refresh(recipe)
        return recipe

    @staticmethod
    def delete_recipe(db: Session, recipe_id: UUID) -> bool:
        """
        Soft delete recipe.

        Args:
            db: Database session
            recipe_id: Recipe to delete

        Returns:
            bool: True if deleted, False if not found
        """
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            return False

        recipe.is_deleted = True
        db.commit()
        return True

    @staticmethod
    def get_recipe_versions(db: Session, recipe_id: UUID) -> List[RecipeVersion]:
        """
        Get all versions of a recipe.

        Args:
            db: Database session
            recipe_id: Recipe ID

        Returns:
            List[RecipeVersion]: List of versions
        """
        return db.query(RecipeVersion).filter(
            RecipeVersion.recipe_id == recipe_id
        ).order_by(RecipeVersion.version_number.desc()).all()

    @staticmethod
    def revert_recipe(
        db: Session,
        recipe_id: UUID,
        version_number: int,
        user_id: UUID
    ) -> Optional[Recipe]:
        """
        Revert recipe to a previous version (creates new version as copy).

        Args:
            db: Database session
            recipe_id: Recipe ID
            version_number: Version to revert to
            user_id: User making the revert

        Returns:
            Optional[Recipe]: Reverted recipe or None if not found
        """
        recipe = db.query(Recipe).filter(
            Recipe.id == recipe_id,
            Recipe.is_deleted == False
        ).first()

        if not recipe:
            return None

        # Get target version
        target_version = db.query(RecipeVersion).filter(
            RecipeVersion.recipe_id == recipe_id,
            RecipeVersion.version_number == version_number
        ).first()

        if not target_version:
            return None

        # Get ingredients from target version
        target_ingredients = db.query(Ingredient).filter(
            Ingredient.recipe_version_id == target_version.id
        ).order_by(Ingredient.display_order).all()

        # Create new version as copy of target
        new_version_number = recipe.current_version + 1

        new_version = RecipeVersion(
            recipe_id=recipe.id,
            version_number=new_version_number,
            prep_time_minutes=target_version.prep_time_minutes,
            cook_time_minutes=target_version.cook_time_minutes,
            servings=target_version.servings,
            difficulty=target_version.difficulty,
            instructions=target_version.instructions,
            change_description=f"Reverted to version {version_number}",
            modified_by=user_id
        )
        db.add(new_version)
        db.flush()

        # Copy ingredients
        for ing in target_ingredients:
            new_ingredient = Ingredient(
                recipe_version_id=new_version.id,
                name=ing.name,
                quantity=ing.quantity,
                unit=ing.unit,
                category=ing.category,
                is_optional=ing.is_optional,
                display_order=ing.display_order
            )
            db.add(new_ingredient)

        # Update recipe
        recipe.current_version = new_version_number

        db.commit()
        db.refresh(recipe)
        return recipe

    @staticmethod
    def get_recipe_suggestions(
        db: Session,
        user_id: UUID,
        limit: int = 10
    ) -> List[Tuple[Recipe, int, List[str]]]:
        """
        Get recipe suggestions based on inventory, favorites, and rotation.

        Args:
            db: Database session
            user_id: Current user ID
            limit: Number of suggestions

        Returns:
            List[Tuple[Recipe, int, List[str]]]: List of (recipe, score, reasons)
        """
        settings = db.query(AppSettings).first()
        rotation_days = settings.rotation_period_days if settings else 14
        cutoff_date = date.today() - timedelta(days=rotation_days)

        suggestions = []

        # Get all non-deleted recipes
        recipes = db.query(Recipe).filter(Recipe.is_deleted == False).all()

        for recipe in recipes:
            score = 0
            reasons = []

            # Not cooked recently (higher priority)
            if not recipe.last_cooked_date or recipe.last_cooked_date <= cutoff_date:
                score += 3
                reasons.append("not_cooked_recently")

            # Is favorite
            ratings = db.query(Rating).filter(Rating.recipe_id == recipe.id).all()
            if ratings and len(ratings) >= 3:
                thumbs_up = sum(1 for r in ratings if r.rating)
                if thumbs_up / len(ratings) >= 0.75:
                    score += 2
                    reasons.append("household_favorite")

            # Never tried
            if recipe.times_cooked == 0:
                score += 1
                reasons.append("never_tried")

            if score > 0:
                suggestions.append((recipe, score, reasons))

        # Sort by score descending
        suggestions.sort(key=lambda x: x[1], reverse=True)

        return suggestions[:limit]

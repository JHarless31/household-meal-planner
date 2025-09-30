"""
Menu Plan Service
Business logic for weekly menu planning and meal tracking
"""

from typing import List, Optional, Tuple, Dict
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from uuid import UUID
from decimal import Decimal
import logging

from src.models.menu_plan import MenuPlan, PlannedMeal
from src.models.recipe import Recipe, RecipeVersion, Ingredient
from src.models.inventory import InventoryItem
from src.schemas.menu_plan import MenuPlanCreate, MenuPlanUpdate, PlannedMealInput
from src.services.inventory_service import InventoryService

logger = logging.getLogger(__name__)


class MenuPlanService:
    """Service for menu planning"""

    @staticmethod
    def create_menu_plan(db: Session, plan_data: MenuPlanCreate, user_id: UUID) -> MenuPlan:
        """Create new menu plan"""
        plan = MenuPlan(
            week_start_date=plan_data.week_start_date,
            name=plan_data.name,
            created_by=user_id
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def get_menu_plan(db: Session, plan_id: UUID) -> Optional[MenuPlan]:
        """Get menu plan by ID"""
        return db.query(MenuPlan).filter(MenuPlan.id == plan_id).first()

    @staticmethod
    def list_menu_plans(
        db: Session,
        week_start: Optional[date] = None,
        active_only: bool = True
    ) -> List[MenuPlan]:
        """List menu plans with filters"""
        query = db.query(MenuPlan)

        if week_start:
            query = query.filter(MenuPlan.week_start_date == week_start)

        if active_only:
            query = query.filter(MenuPlan.is_active == True)

        return query.order_by(MenuPlan.week_start_date.desc()).all()

    @staticmethod
    def update_menu_plan(
        db: Session,
        plan_id: UUID,
        plan_data: MenuPlanUpdate
    ) -> Optional[MenuPlan]:
        """Update menu plan"""
        plan = db.query(MenuPlan).filter(MenuPlan.id == plan_id).first()
        if not plan:
            return None

        # Update basic fields
        if plan_data.name is not None:
            plan.name = plan_data.name

        if plan_data.is_active is not None:
            plan.is_active = plan_data.is_active

        # Update meals if provided
        if plan_data.meals is not None:
            # Remove existing meals
            db.query(PlannedMeal).filter(PlannedMeal.menu_plan_id == plan_id).delete()

            # Add new meals
            for meal_data in plan_data.meals:
                meal = PlannedMeal(
                    menu_plan_id=plan_id,
                    recipe_id=meal_data.recipe_id,
                    meal_date=meal_data.meal_date,
                    meal_type=meal_data.meal_type,
                    servings_planned=meal_data.servings_planned,
                    notes=meal_data.notes
                )
                db.add(meal)

        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def delete_menu_plan(db: Session, plan_id: UUID) -> bool:
        """Delete menu plan"""
        plan = db.query(MenuPlan).filter(MenuPlan.id == plan_id).first()
        if not plan:
            return False

        db.delete(plan)
        db.commit()
        return True

    @staticmethod
    def add_meal_to_plan(
        db: Session,
        plan_id: UUID,
        meal_data: PlannedMealInput
    ) -> Optional[PlannedMeal]:
        """Add meal to menu plan"""
        # Verify plan exists
        plan = db.query(MenuPlan).filter(MenuPlan.id == plan_id).first()
        if not plan:
            return None

        # Verify recipe exists
        recipe = db.query(Recipe).filter(
            Recipe.id == meal_data.recipe_id,
            Recipe.is_deleted == False
        ).first()
        if not recipe:
            return None

        meal = PlannedMeal(
            menu_plan_id=plan_id,
            recipe_id=meal_data.recipe_id,
            meal_date=meal_data.meal_date,
            meal_type=meal_data.meal_type,
            servings_planned=meal_data.servings_planned,
            notes=meal_data.notes
        )
        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal

    @staticmethod
    def mark_meal_cooked(
        db: Session,
        plan_id: UUID,
        meal_id: UUID,
        user_id: UUID
    ) -> Tuple[Optional[PlannedMeal], List[Dict]]:
        """
        Mark meal as cooked and auto-deduct ingredients from inventory.

        Returns:
            Tuple of (meal, inventory_changes)
        """
        meal = db.query(PlannedMeal).filter(
            PlannedMeal.id == meal_id,
            PlannedMeal.menu_plan_id == plan_id
        ).first()

        if not meal:
            return None, []

        # Mark as cooked
        meal.cooked = True
        meal.cooked_date = datetime.now()
        meal.cooked_by = user_id

        # Update recipe stats
        recipe = db.query(Recipe).filter(Recipe.id == meal.recipe_id).first()
        if recipe:
            recipe.last_cooked_date = date.today()
            recipe.times_cooked = (recipe.times_cooked or 0) + 1

        # Get recipe ingredients for current version
        version = db.query(RecipeVersion).filter(
            RecipeVersion.recipe_id == meal.recipe_id,
            RecipeVersion.version_number == recipe.current_version
        ).first()

        inventory_changes = []

        if version:
            ingredients = db.query(Ingredient).filter(
                Ingredient.recipe_version_id == version.id
            ).all()

            # Deduct ingredients from inventory
            for ing in ingredients:
                if ing.is_optional:
                    continue  # Don't deduct optional ingredients

                # Try to find matching inventory item
                item = db.query(InventoryItem).filter(
                    InventoryItem.item_name.ilike(ing.name)
                ).first()

                if item and ing.quantity:
                    # Calculate quantity to deduct (adjust for servings)
                    servings_ratio = (meal.servings_planned or version.servings or 1) / (version.servings or 1)
                    quantity_to_deduct = Decimal(str(ing.quantity)) * Decimal(str(servings_ratio))

                    # Deduct from inventory
                    success = InventoryService.deduct_quantity(
                        db,
                        item.id,
                        quantity_to_deduct,
                        f"Used for {recipe.title}",
                        user_id
                    )

                    if success:
                        inventory_changes.append({
                            "item_name": item.item_name,
                            "quantity_deducted": float(quantity_to_deduct)
                        })

        db.commit()
        db.refresh(meal)
        return meal, inventory_changes

    @staticmethod
    def remove_meal_from_plan(db: Session, meal_id: UUID) -> bool:
        """Remove meal from plan"""
        meal = db.query(PlannedMeal).filter(PlannedMeal.id == meal_id).first()
        if not meal:
            return False

        db.delete(meal)
        db.commit()
        return True

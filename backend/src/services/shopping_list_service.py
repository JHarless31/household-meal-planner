"""
Shopping List Service
Business logic for generating shopping lists from menu plans
"""

from typing import List, Dict
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from collections import defaultdict
import logging

from src.models.menu_plan import MenuPlan, PlannedMeal
from src.models.recipe import Recipe, RecipeVersion, Ingredient
from src.models.inventory import InventoryItem
from src.schemas.shopping_list import ShoppingListItem, ShoppingListResponse

logger = logging.getLogger(__name__)


class ShoppingListService:
    """Service for shopping list generation"""

    @staticmethod
    def generate_shopping_list(
        db: Session,
        plan_id: UUID,
        grouped: bool = True
    ) -> ShoppingListResponse:
        """
        Generate shopping list for menu plan.

        Aggregates ingredients needed for all meals in plan and
        compares against current inventory.

        Args:
            db: Database session
            plan_id: Menu plan ID
            grouped: Whether to group by category

        Returns:
            ShoppingListResponse: Generated shopping list
        """
        plan = db.query(MenuPlan).filter(MenuPlan.id == plan_id).first()
        if not plan:
            raise ValueError("Menu plan not found")

        # Get all meals in the plan that haven't been cooked
        meals = db.query(PlannedMeal).filter(
            PlannedMeal.menu_plan_id == plan_id,
            PlannedMeal.cooked == False
        ).all()

        # Aggregate ingredients by name
        # Structure: {ingredient_name: {quantity, unit, category, recipes[]}}
        aggregated = defaultdict(lambda: {
            "quantity": Decimal(0),
            "unit": None,
            "category": "other",
            "recipes": []
        })

        for meal in meals:
            recipe = db.query(Recipe).filter(Recipe.id == meal.recipe_id).first()
            if not recipe:
                continue

            # Get recipe version
            version = db.query(RecipeVersion).filter(
                RecipeVersion.recipe_id == recipe.id,
                RecipeVersion.version_number == recipe.current_version
            ).first()

            if not version:
                continue

            # Get ingredients
            ingredients = db.query(Ingredient).filter(
                Ingredient.recipe_version_id == version.id,
                Ingredient.is_optional == False  # Skip optional ingredients
            ).all()

            # Calculate servings ratio
            servings_ratio = (meal.servings_planned or version.servings or 1) / (version.servings or 1)

            for ing in ingredients:
                key = ing.name.lower().strip()

                # Aggregate quantity
                if ing.quantity:
                    quantity = Decimal(str(ing.quantity)) * Decimal(str(servings_ratio))
                    aggregated[key]["quantity"] += quantity

                # Set unit and category (use first encountered)
                if not aggregated[key]["unit"] and ing.unit:
                    aggregated[key]["unit"] = ing.unit
                if ing.category:
                    aggregated[key]["category"] = ing.category

                # Track which recipes need this ingredient
                if recipe.title not in aggregated[key]["recipes"]:
                    aggregated[key]["recipes"].append(recipe.title)

        # Check against inventory
        shopping_items = []

        for name, data in aggregated.items():
            # Try to find item in inventory
            item = db.query(InventoryItem).filter(
                InventoryItem.item_name.ilike(name)
            ).first()

            in_stock = False
            quantity_needed = data["quantity"]

            if item:
                # Check if we have enough in stock
                if item.quantity >= quantity_needed:
                    in_stock = True
                    continue  # Don't add to shopping list if we have enough
                else:
                    # Calculate deficit
                    quantity_needed = quantity_needed - item.quantity
                    if quantity_needed <= 0:
                        continue

            shopping_item = ShoppingListItem(
                id=uuid4(),
                name=name.title(),
                quantity=quantity_needed,
                unit=data["unit"] or "",
                category=data["category"],
                needed_for_recipes=data["recipes"],
                in_stock=in_stock,
                checked=False
            )
            shopping_items.append(shopping_item)

        # Sort by category if grouped
        if grouped:
            shopping_items.sort(key=lambda x: (x.category, x.name))
        else:
            shopping_items.sort(key=lambda x: x.name)

        return ShoppingListResponse(
            menu_plan_id=plan_id,
            items=shopping_items,
            generated_at=datetime.now()
        )

    @staticmethod
    def mark_item_purchased(
        db: Session,
        item_name: str,
        quantity: Decimal,
        unit: Optional[str],
        category: Optional[str],
        user_id: UUID
    ) -> bool:
        """
        Mark shopping list item as purchased and add to inventory.

        Args:
            db: Database session
            item_name: Item name
            quantity: Quantity purchased
            unit: Unit of measurement
            category: Item category
            user_id: User who made the purchase

        Returns:
            bool: True if successful
        """
        from src.services.inventory_service import InventoryService

        # Find or create inventory item
        item = db.query(InventoryItem).filter(
            InventoryItem.item_name.ilike(item_name)
        ).first()

        if item:
            # Add to existing quantity
            from src.models.inventory import InventoryHistory

            old_quantity = item.quantity
            item.quantity += quantity

            # Log purchase
            history = InventoryHistory(
                inventory_id=item.id,
                change_type="purchased",
                quantity_before=old_quantity,
                quantity_after=item.quantity,
                reason="Shopping list purchase",
                changed_by=user_id
            )
            db.add(history)
        else:
            # Create new inventory item
            from src.schemas.inventory import InventoryItemCreate

            item_data = InventoryItemCreate(
                item_name=item_name,
                quantity=quantity,
                unit=unit,
                category=category
            )
            item = InventoryService.create_item(db, item_data, user_id)

        db.commit()
        return True

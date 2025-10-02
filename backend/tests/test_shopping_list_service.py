"""
Unit Tests for Shopping List Service
Tests shopping list generation and inventory integration
"""

from decimal import Decimal
from uuid import uuid4

import pytest

from src.models.inventory import InventoryItem
from src.services.shopping_list_service import ShoppingListService


@pytest.mark.unit
class TestShoppingListService:
    """Test cases for shopping list service"""

    def test_generate_shopping_list_success(self, db, test_planned_meal):
        """Test successful shopping list generation"""
        result = ShoppingListService.generate_shopping_list(
            db, test_planned_meal.menu_plan_id
        )

        assert result is not None
        assert result.menu_plan_id == test_planned_meal.menu_plan_id
        assert len(result.items) > 0

    def test_generate_shopping_list_aggregates_ingredients(
        self, db, test_user, test_recipe
    ):
        """Test that shopping list aggregates same ingredients"""
        from datetime import date

        from src.models.menu_plan import MenuPlan, PlannedMeal

        plan = MenuPlan(
            week_start_date=date.today(), name="Test Plan", created_by=test_user.id
        )
        db.add(plan)
        db.flush()

        # Add same recipe twice
        for i in range(2):
            meal = PlannedMeal(
                menu_plan_id=plan.id,
                recipe_id=test_recipe.id,
                meal_date=date.today(),
                meal_type="dinner",
                servings_planned=4,
                cooked=False,
            )
            db.add(meal)

        db.commit()

        result = ShoppingListService.generate_shopping_list(db, plan.id)

        # Should aggregate quantities for same ingredients
        assert len(result.items) == 3  # chicken, rice, vegetables

    def test_generate_shopping_list_checks_inventory(self, db, test_user, test_recipe):
        """Test that shopping list checks against inventory"""
        from datetime import date

        from src.models.menu_plan import MenuPlan, PlannedMeal

        plan = MenuPlan(
            week_start_date=date.today(), name="Test Plan", created_by=test_user.id
        )
        db.add(plan)
        db.flush()

        meal = PlannedMeal(
            menu_plan_id=plan.id,
            recipe_id=test_recipe.id,
            meal_date=date.today(),
            meal_type="dinner",
            servings_planned=4,
            cooked=False,
        )
        db.add(meal)

        # Add inventory for one ingredient (enough stock)
        item = InventoryItem(
            item_name="chicken", quantity=Decimal("1000"), unit="g", category="meat"
        )
        db.add(item)
        db.commit()

        result = ShoppingListService.generate_shopping_list(db, plan.id)

        # Should not include chicken (we have enough)
        item_names = [item.name.lower() for item in result.items]
        assert "chicken" not in item_names

    def test_generate_shopping_list_calculates_deficit(
        self, db, test_user, test_recipe
    ):
        """Test shopping list calculates deficit when partial stock"""
        from datetime import date

        from src.models.menu_plan import MenuPlan, PlannedMeal

        plan = MenuPlan(
            week_start_date=date.today(), name="Test Plan", created_by=test_user.id
        )
        db.add(plan)
        db.flush()

        meal = PlannedMeal(
            menu_plan_id=plan.id,
            recipe_id=test_recipe.id,
            meal_date=date.today(),
            meal_type="dinner",
            servings_planned=4,
            cooked=False,
        )
        db.add(meal)

        # Add partial inventory (need 200g, have 100g)
        item = InventoryItem(
            item_name="rice", quantity=Decimal("100"), unit="g", category="grain"
        )
        db.add(item)
        db.commit()

        result = ShoppingListService.generate_shopping_list(db, plan.id)

        # Should include rice with deficit quantity
        rice_item = next(
            (item for item in result.items if item.name.lower() == "rice"), None
        )
        assert rice_item is not None
        assert rice_item.quantity == Decimal("100")  # Need 200 - have 100

    def test_generate_shopping_list_skips_cooked_meals(self, db, test_planned_meal):
        """Test that shopping list skips cooked meals"""
        # Mark meal as cooked
        test_planned_meal.cooked = True
        db.commit()

        result = ShoppingListService.generate_shopping_list(
            db, test_planned_meal.menu_plan_id
        )

        # Should have no items (only meal is cooked)
        assert len(result.items) == 0

    def test_generate_shopping_list_skips_optional_ingredients(
        self, db, test_user, test_recipe
    ):
        """Test that shopping list skips optional ingredients"""
        from datetime import date

        from src.models.menu_plan import MenuPlan, PlannedMeal
        from src.models.recipe import Ingredient, RecipeVersion

        # Make one ingredient optional
        version = (
            db.query(RecipeVersion)
            .filter(RecipeVersion.recipe_id == test_recipe.id)
            .first()
        )
        ing = (
            db.query(Ingredient)
            .filter(Ingredient.recipe_version_id == version.id)
            .first()
        )
        ing.is_optional = True
        db.commit()

        plan = MenuPlan(
            week_start_date=date.today(), name="Test Plan", created_by=test_user.id
        )
        db.add(plan)
        db.flush()

        meal = PlannedMeal(
            menu_plan_id=plan.id,
            recipe_id=test_recipe.id,
            meal_date=date.today(),
            meal_type="dinner",
            servings_planned=4,
            cooked=False,
        )
        db.add(meal)
        db.commit()

        result = ShoppingListService.generate_shopping_list(db, plan.id)

        # Should have fewer items (optional ingredient excluded)
        assert len(result.items) < 3

    def test_generate_shopping_list_grouped(self, db, test_planned_meal):
        """Test that shopping list can be grouped by category"""
        result = ShoppingListService.generate_shopping_list(
            db, test_planned_meal.menu_plan_id, grouped=True
        )

        # Items should be sorted by category
        categories = [item.category for item in result.items]
        assert categories == sorted(categories)

    def test_generate_shopping_list_ungrouped(self, db, test_planned_meal):
        """Test that shopping list can be ungrouped"""
        result = ShoppingListService.generate_shopping_list(
            db, test_planned_meal.menu_plan_id, grouped=False
        )

        # Items should be sorted by name
        names = [item.name for item in result.items]
        assert names == sorted(names)

    def test_generate_shopping_list_not_found(self, db):
        """Test generating shopping list for non-existent plan"""
        with pytest.raises(ValueError):
            ShoppingListService.generate_shopping_list(db, uuid4())

    def test_mark_item_purchased_updates_inventory(self, db, test_user):
        """Test marking item purchased updates inventory"""
        result = ShoppingListService.mark_item_purchased(
            db, "New Item", Decimal("5"), "pcs", "other", test_user.id
        )

        assert result is True

        # Check inventory item created
        item = (
            db.query(InventoryItem)
            .filter(InventoryItem.item_name == "New Item")
            .first()
        )
        assert item is not None
        assert item.quantity == Decimal("5")

    def test_mark_item_purchased_adds_to_existing(self, db, test_user):
        """Test marking item purchased adds to existing inventory"""
        # Create existing inventory
        item = InventoryItem(
            item_name="Existing Item",
            quantity=Decimal("10"),
            unit="pcs",
            category="other",
        )
        db.add(item)
        db.commit()

        result = ShoppingListService.mark_item_purchased(
            db, "Existing Item", Decimal("5"), "pcs", "other", test_user.id
        )

        assert result is True

        # Check quantity added
        item = (
            db.query(InventoryItem)
            .filter(InventoryItem.item_name == "Existing Item")
            .first()
        )
        assert item.quantity == Decimal("15")

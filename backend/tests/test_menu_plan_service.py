"""
Unit Tests for Menu Plan Service
Tests menu planning, meal tracking, and auto-deduction
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

from src.services.menu_plan_service import MenuPlanService
from src.schemas.menu_plan import MenuPlanCreate, MenuPlanUpdate, PlannedMealInput
from src.models.menu_plan import MenuPlan, PlannedMeal
from src.models.recipe import Recipe
from src.models.inventory import InventoryItem


@pytest.mark.unit
class TestMenuPlanService:
    """Test cases for menu plan service"""

    def test_create_menu_plan_success(self, db, test_user):
        """Test successful menu plan creation"""
        plan_data = MenuPlanCreate(
            week_start_date=date.today(),
            name="Test Menu Plan"
        )

        plan = MenuPlanService.create_menu_plan(db, plan_data, test_user.id)

        assert plan.id is not None
        assert plan.name == "Test Menu Plan"
        assert plan.created_by == test_user.id
        assert plan.is_active is True

    def test_get_menu_plan_success(self, db, test_menu_plan):
        """Test successful menu plan retrieval"""
        plan = MenuPlanService.get_menu_plan(db, test_menu_plan.id)

        assert plan is not None
        assert plan.id == test_menu_plan.id

    def test_get_menu_plan_not_found(self, db):
        """Test getting non-existent menu plan"""
        plan = MenuPlanService.get_menu_plan(db, uuid4())

        assert plan is None

    def test_list_menu_plans_all(self, db, test_user):
        """Test listing all menu plans"""
        # Create multiple plans
        for i in range(3):
            plan_data = MenuPlanCreate(
                week_start_date=date.today() + timedelta(weeks=i),
                name=f"Plan {i}"
            )
            MenuPlanService.create_menu_plan(db, plan_data, test_user.id)

        plans = MenuPlanService.list_menu_plans(db)

        assert len(plans) == 3

    def test_list_menu_plans_filter_week(self, db, test_user):
        """Test filtering plans by week"""
        week1 = date.today()
        week2 = date.today() + timedelta(weeks=1)

        plan_data1 = MenuPlanCreate(week_start_date=week1, name="Week 1")
        plan_data2 = MenuPlanCreate(week_start_date=week2, name="Week 2")

        MenuPlanService.create_menu_plan(db, plan_data1, test_user.id)
        MenuPlanService.create_menu_plan(db, plan_data2, test_user.id)

        plans = MenuPlanService.list_menu_plans(db, week_start=week1)

        assert len(plans) == 1
        assert plans[0].name == "Week 1"

    def test_list_menu_plans_active_only(self, db, test_user):
        """Test filtering active plans only"""
        plan_data = MenuPlanCreate(week_start_date=date.today(), name="Plan 1")
        plan1 = MenuPlanService.create_menu_plan(db, plan_data, test_user.id)

        plan_data = MenuPlanCreate(week_start_date=date.today(), name="Plan 2")
        plan2 = MenuPlanService.create_menu_plan(db, plan_data, test_user.id)

        # Deactivate plan2
        plan2.is_active = False
        db.commit()

        plans = MenuPlanService.list_menu_plans(db, active_only=True)

        assert len(plans) == 1
        assert plans[0].id == plan1.id

    def test_update_menu_plan_name(self, db, test_menu_plan):
        """Test updating menu plan name"""
        plan_data = MenuPlanUpdate(name="Updated Name")

        updated = MenuPlanService.update_menu_plan(db, test_menu_plan.id, plan_data)

        assert updated is not None
        assert updated.name == "Updated Name"

    def test_update_menu_plan_is_active(self, db, test_menu_plan):
        """Test updating menu plan active status"""
        plan_data = MenuPlanUpdate(is_active=False)

        updated = MenuPlanService.update_menu_plan(db, test_menu_plan.id, plan_data)

        assert updated is not None
        assert updated.is_active is False

    def test_update_menu_plan_not_found(self, db):
        """Test updating non-existent menu plan"""
        plan_data = MenuPlanUpdate(name="Updated")

        updated = MenuPlanService.update_menu_plan(db, uuid4(), plan_data)

        assert updated is None

    def test_delete_menu_plan_success(self, db, test_menu_plan):
        """Test successful menu plan deletion"""
        result = MenuPlanService.delete_menu_plan(db, test_menu_plan.id)

        assert result is True

        plan = db.query(MenuPlan).filter(MenuPlan.id == test_menu_plan.id).first()
        assert plan is None

    def test_delete_menu_plan_not_found(self, db):
        """Test deleting non-existent menu plan"""
        result = MenuPlanService.delete_menu_plan(db, uuid4())

        assert result is False

    def test_add_meal_to_plan_success(self, db, test_menu_plan, test_recipe):
        """Test successfully adding meal to plan"""
        meal_data = PlannedMealInput(
            recipe_id=test_recipe.id,
            meal_date=date.today(),
            meal_type="dinner",
            servings_planned=4,
            notes="Test notes"
        )

        meal = MenuPlanService.add_meal_to_plan(db, test_menu_plan.id, meal_data)

        assert meal is not None
        assert meal.recipe_id == test_recipe.id
        assert meal.menu_plan_id == test_menu_plan.id
        assert meal.meal_type == "dinner"

    def test_add_meal_plan_not_found(self, db, test_recipe):
        """Test adding meal to non-existent plan"""
        meal_data = PlannedMealInput(
            recipe_id=test_recipe.id,
            meal_date=date.today(),
            meal_type="dinner",
            servings_planned=4
        )

        meal = MenuPlanService.add_meal_to_plan(db, uuid4(), meal_data)

        assert meal is None

    def test_add_meal_recipe_not_found(self, db, test_menu_plan):
        """Test adding meal with non-existent recipe"""
        meal_data = PlannedMealInput(
            recipe_id=uuid4(),
            meal_date=date.today(),
            meal_type="dinner",
            servings_planned=4
        )

        meal = MenuPlanService.add_meal_to_plan(db, test_menu_plan.id, meal_data)

        assert meal is None

    def test_mark_meal_cooked_success(self, db, test_planned_meal, test_user):
        """Test marking meal as cooked"""
        meal, changes = MenuPlanService.mark_meal_cooked(
            db, test_planned_meal.menu_plan_id, test_planned_meal.id, test_user.id
        )

        assert meal is not None
        assert meal.cooked is True
        assert meal.cooked_by == test_user.id

        # Check recipe stats updated
        recipe = db.query(Recipe).filter(Recipe.id == test_planned_meal.recipe_id).first()
        assert recipe.times_cooked == 1
        assert recipe.last_cooked_date == date.today()

    def test_mark_meal_cooked_deducts_inventory(self, db, test_user, test_recipe):
        """Test that marking meal cooked deducts inventory"""
        # Create inventory items matching recipe ingredients
        for ing_name in ["chicken", "rice", "vegetables"]:
            item = InventoryItem(
                item_name=ing_name,
                quantity=Decimal("1000"),
                unit="g",
                category="other"
            )
            db.add(item)
        db.commit()

        # Create menu plan and meal
        plan_data = MenuPlanCreate(week_start_date=date.today(), name="Test")
        plan = MenuPlanService.create_menu_plan(db, plan_data, test_user.id)

        meal_data = PlannedMealInput(
            recipe_id=test_recipe.id,
            meal_date=date.today(),
            meal_type="dinner",
            servings_planned=4
        )
        meal = MenuPlanService.add_meal_to_plan(db, plan.id, meal_data)

        # Mark as cooked
        meal_result, changes = MenuPlanService.mark_meal_cooked(
            db, plan.id, meal.id, test_user.id
        )

        assert len(changes) == 3
        # Check inventory was deducted
        chicken = db.query(InventoryItem).filter(
            InventoryItem.item_name == "chicken"
        ).first()
        assert chicken.quantity < Decimal("1000")

    def test_mark_meal_cooked_not_found(self, db, test_user):
        """Test marking non-existent meal as cooked"""
        meal, changes = MenuPlanService.mark_meal_cooked(
            db, uuid4(), uuid4(), test_user.id
        )

        assert meal is None
        assert changes == []

    def test_remove_meal_from_plan_success(self, db, test_planned_meal):
        """Test removing meal from plan"""
        result = MenuPlanService.remove_meal_from_plan(db, test_planned_meal.id)

        assert result is True

        meal = db.query(PlannedMeal).filter(
            PlannedMeal.id == test_planned_meal.id
        ).first()
        assert meal is None

    def test_remove_meal_not_found(self, db):
        """Test removing non-existent meal"""
        result = MenuPlanService.remove_meal_from_plan(db, uuid4())

        assert result is False

    def test_copy_menu_plan_success(self, db, test_user, test_recipe):
        """Test copying menu plan to new week"""
        # Create source plan with meals
        plan_data = MenuPlanCreate(
            week_start_date=date.today(),
            name="Original Plan"
        )
        source_plan = MenuPlanService.create_menu_plan(db, plan_data, test_user.id)

        # Add meals
        for i in range(3):
            meal_data = PlannedMealInput(
                recipe_id=test_recipe.id,
                meal_date=date.today() + timedelta(days=i),
                meal_type="dinner",
                servings_planned=4
            )
            MenuPlanService.add_meal_to_plan(db, source_plan.id, meal_data)

        # Copy to new week
        new_week = date.today() + timedelta(weeks=1)
        new_plan = MenuPlanService.copy_menu_plan(
            db, source_plan.id, new_week, test_user.id
        )

        assert new_plan is not None
        assert new_plan.id != source_plan.id
        assert new_plan.week_start_date == new_week
        assert "(Copy)" in new_plan.name

        # Check meals were copied
        new_meals = db.query(PlannedMeal).filter(
            PlannedMeal.menu_plan_id == new_plan.id
        ).all()
        assert len(new_meals) == 3

        # Check dates were adjusted
        for meal in new_meals:
            assert meal.meal_date >= new_week

    def test_copy_menu_plan_not_found(self, db, test_user):
        """Test copying non-existent plan"""
        new_plan = MenuPlanService.copy_menu_plan(
            db, uuid4(), date.today(), test_user.id
        )

        assert new_plan is None

    def test_suggest_week_plan_success(self, db, test_user, test_recipes):
        """Test auto-generating week plan"""
        plan = MenuPlanService.suggest_week_plan(
            db, date.today(), test_user.id, strategy="rotation"
        )

        assert plan is not None
        assert "Suggested Plan" in plan.name

        # Check meals were added
        meals = db.query(PlannedMeal).filter(
            PlannedMeal.menu_plan_id == plan.id
        ).all()
        assert len(meals) > 0

    def test_suggest_week_plan_variety_enforcement(self, db, test_user, test_recipes):
        """Test that suggested plan enforces variety (no duplicate recipes)"""
        plan = MenuPlanService.suggest_week_plan(
            db, date.today(), test_user.id, strategy="rotation"
        )

        meals = db.query(PlannedMeal).filter(
            PlannedMeal.menu_plan_id == plan.id
        ).all()

        # Check no recipe appears twice
        recipe_ids = [meal.recipe_id for meal in meals]
        assert len(recipe_ids) == len(set(recipe_ids))

    def test_suggest_week_plan_no_recipes(self, db, test_user):
        """Test suggesting plan with no available recipes"""
        plan = MenuPlanService.suggest_week_plan(
            db, date.today(), test_user.id, strategy="rotation"
        )

        assert plan is not None

        # Should create empty plan
        meals = db.query(PlannedMeal).filter(
            PlannedMeal.menu_plan_id == plan.id
        ).all()
        assert len(meals) == 0

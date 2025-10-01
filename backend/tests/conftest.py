"""
Pytest Configuration and Fixtures
Comprehensive test fixtures for all models and services
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import date, datetime, timedelta
from decimal import Decimal
from faker import Faker

from src.main import app
from src.core.database import Base, get_db
from src.models.user import User
from src.models.recipe import Recipe, RecipeVersion, Ingredient, RecipeTag
from src.models.inventory import InventoryItem, InventoryHistory
from src.models.rating import Rating
from src.models.menu_plan import MenuPlan, PlannedMeal
from src.models.notification import Notification
from src.models.app_settings import AppSettings
from src.core.security import SecurityManager

fake = Faker()

# Test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    # Create default app settings
    settings = AppSettings(
        rotation_period_days=14,
        favorites_threshold=0.75,
        favorites_min_raters=3,
        expiration_warning_days=7,
        low_stock_threshold=0.2
    )
    session.add(settings)
    session.commit()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client"""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ===== User Fixtures =====

@pytest.fixture
def test_user(db):
    """Create test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=SecurityManager.hash_password("testpassword123"),
        role="user",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_user(db):
    """Create admin user"""
    user = User(
        username="admin",
        email="admin@example.com",
        password_hash=SecurityManager.hash_password("adminpassword123"),
        role="admin",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def inactive_user(db):
    """Create inactive user"""
    user = User(
        username="inactive",
        email="inactive@example.com",
        password_hash=SecurityManager.hash_password("password123"),
        role="user",
        is_active=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers"""
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    return {"Cookie": response.cookies.get("session")}


@pytest.fixture
def admin_headers(client, admin_user):
    """Get admin authentication headers"""
    response = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "adminpassword123"
    })
    assert response.status_code == 200
    return {"Cookie": response.cookies.get("session")}


# ===== Recipe Fixtures =====

@pytest.fixture
def test_recipe(db, test_user):
    """Create a test recipe with version 1"""
    recipe = Recipe(
        title="Test Recipe",
        description="A delicious test recipe",
        created_by=test_user.id,
        current_version=1,
        source_type="manual"
    )
    db.add(recipe)
    db.flush()

    # Create version 1
    version = RecipeVersion(
        recipe_id=recipe.id,
        version_number=1,
        prep_time_minutes=15,
        cook_time_minutes=30,
        servings=4,
        difficulty="medium",
        instructions="1. Prepare ingredients\n2. Cook\n3. Serve",
        modified_by=test_user.id
    )
    db.add(version)
    db.flush()

    # Add ingredients
    ingredients = [
        Ingredient(
            recipe_version_id=version.id,
            name="chicken",
            quantity=500,
            unit="g",
            category="meat",
            display_order=0
        ),
        Ingredient(
            recipe_version_id=version.id,
            name="rice",
            quantity=200,
            unit="g",
            category="grain",
            display_order=1
        ),
        Ingredient(
            recipe_version_id=version.id,
            name="vegetables",
            quantity=300,
            unit="g",
            category="vegetable",
            display_order=2
        )
    ]
    db.add_all(ingredients)

    # Add tags
    tags = [
        RecipeTag(recipe_id=recipe.id, tag="dinner"),
        RecipeTag(recipe_id=recipe.id, tag="easy")
    ]
    db.add_all(tags)

    db.commit()
    db.refresh(recipe)
    return recipe


@pytest.fixture
def test_recipes(db, test_user):
    """Create multiple test recipes"""
    recipes = []

    recipe_data = [
        ("Pasta Carbonara", "Italian classic", "easy", 20, 15, 2),
        ("Beef Stew", "Hearty stew", "hard", 30, 120, 6),
        ("Quick Salad", "Fresh salad", "easy", 10, 0, 2),
        ("Roast Chicken", "Sunday roast", "medium", 20, 60, 4),
        ("Vegetable Curry", "Spicy curry", "medium", 15, 25, 4)
    ]

    for title, desc, difficulty, prep, cook, servings in recipe_data:
        recipe = Recipe(
            title=title,
            description=desc,
            created_by=test_user.id,
            current_version=1,
            source_type="manual"
        )
        db.add(recipe)
        db.flush()

        version = RecipeVersion(
            recipe_id=recipe.id,
            version_number=1,
            prep_time_minutes=prep,
            cook_time_minutes=cook,
            servings=servings,
            difficulty=difficulty,
            instructions=f"Instructions for {title}",
            modified_by=test_user.id
        )
        db.add(version)
        db.flush()

        # Add some ingredients
        ing = Ingredient(
            recipe_version_id=version.id,
            name=title.split()[0].lower(),
            quantity=100,
            unit="g",
            category="other",
            display_order=0
        )
        db.add(ing)

        recipes.append(recipe)

    db.commit()
    for recipe in recipes:
        db.refresh(recipe)

    return recipes


# ===== Inventory Fixtures =====

@pytest.fixture
def test_inventory_item(db, test_user):
    """Create a test inventory item"""
    item = InventoryItem(
        item_name="Tomatoes",
        quantity=Decimal("10"),
        unit="pcs",
        category="vegetable",
        location="fridge",
        minimum_stock=Decimal("5"),
        expiration_date=date.today() + timedelta(days=5)
    )
    db.add(item)
    db.flush()

    # Add initial history
    history = InventoryHistory(
        inventory_id=item.id,
        change_type="purchased",
        quantity_before=Decimal("0"),
        quantity_after=Decimal("10"),
        reason="Initial stock",
        changed_by=test_user.id
    )
    db.add(history)

    db.commit()
    db.refresh(item)
    return item


@pytest.fixture
def test_inventory_items(db, test_user):
    """Create multiple test inventory items"""
    items = []

    item_data = [
        ("Milk", 2, "L", "dairy", "fridge", 1, 3),
        ("Eggs", 12, "pcs", "dairy", "fridge", 6, 7),
        ("Flour", 1000, "g", "grain", "pantry", 500, None),
        ("Chicken Breast", 500, "g", "meat", "freezer", 200, 14),
        ("Olive Oil", 500, "ml", "oil", "pantry", 100, None)
    ]

    for name, qty, unit, cat, loc, min_stock, exp_days in item_data:
        item = InventoryItem(
            item_name=name,
            quantity=Decimal(str(qty)),
            unit=unit,
            category=cat,
            location=loc,
            minimum_stock=Decimal(str(min_stock)),
            expiration_date=date.today() + timedelta(days=exp_days) if exp_days else None
        )
        db.add(item)
        items.append(item)

    db.commit()
    for item in items:
        db.refresh(item)

    return items


# ===== Rating Fixtures =====

@pytest.fixture
def test_rating(db, test_recipe, test_user):
    """Create a test rating"""
    rating = Rating(
        recipe_id=test_recipe.id,
        user_id=test_user.id,
        rating=True,
        feedback="Great recipe!"
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


# ===== Menu Plan Fixtures =====

@pytest.fixture
def test_menu_plan(db, test_user):
    """Create a test menu plan"""
    plan = MenuPlan(
        week_start_date=date.today(),
        name="This Week's Menu",
        created_by=test_user.id,
        is_active=True
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@pytest.fixture
def test_planned_meal(db, test_menu_plan, test_recipe):
    """Create a test planned meal"""
    meal = PlannedMeal(
        menu_plan_id=test_menu_plan.id,
        recipe_id=test_recipe.id,
        meal_date=date.today(),
        meal_type="dinner",
        servings_planned=4,
        cooked=False
    )
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal


# ===== Notification Fixtures =====

@pytest.fixture
def test_notification(db, test_user):
    """Create a test notification"""
    notification = Notification(
        user_id=test_user.id,
        type="low_stock",
        title="Low Stock Alert",
        message="Milk is running low",
        link="/inventory",
        is_read=False
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


# ===== Mock Fixtures =====

@pytest.fixture
def mock_time(monkeypatch):
    """Mock datetime.now() for consistent testing"""
    class MockDatetime:
        @classmethod
        def now(cls):
            return datetime(2025, 1, 1, 12, 0, 0)

        @classmethod
        def today(cls):
            return date(2025, 1, 1)

    monkeypatch.setattr("datetime.datetime", MockDatetime)
    return MockDatetime

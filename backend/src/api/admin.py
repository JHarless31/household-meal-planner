"""Admin API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from datetime import datetime, timedelta

from src.core.database import get_db
from src.core.security import get_current_user, require_admin
from src.models.user import User
from src.models.app_settings import AppSettings
from src.models.recipe import Recipe
from src.models.rating import Rating
from src.models.menu_plan import MenuPlan
from src.models.inventory import InventoryItem
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.schemas.app_settings import AppSettingsResponse, AppSettingsUpdate

router = APIRouter()

@router.get("/users", response_model=dict)
async def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    users = db.query(User).all()
    return {"users": [UserResponse.model_validate(u) for u in users]}

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    from src.core.security import SecurityManager
    user = User(username=user_data.username, email=user_data.email, password_hash=SecurityManager.hash_password(user_data.password), role=user_data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/settings", response_model=AppSettingsResponse)
async def get_settings(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    settings = db.query(AppSettings).first()
    if not settings: raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.put("/settings", response_model=AppSettingsResponse)
async def update_settings(settings_data: AppSettingsUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    settings = db.query(AppSettings).first()
    if not settings: settings = AppSettings()
    for field, value in settings_data.model_dump().items():
        setattr(settings, field, value)
    settings.updated_by = admin.id
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings

@router.get("/statistics", response_model=dict)
async def get_system_statistics(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """
    Get system statistics for admin dashboard.

    Returns comprehensive statistics including:
    - Total counts for users, recipes, menu plans, inventory items
    - Most popular recipes (by times_cooked)
    - Most favorited recipes (by average rating)
    - Active users (logged in last 30 days)
    - Recent activity metrics
    """
    # Total counts
    total_users = db.query(func.count(User.id)).scalar()
    total_recipes = db.query(func.count(Recipe.id)).filter(Recipe.is_deleted == False).scalar()
    total_menu_plans = db.query(func.count(MenuPlan.id)).scalar()
    total_inventory_items = db.query(func.count(InventoryItem.id)).scalar()

    # Active users (logged in last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    active_users = db.query(func.count(User.id)).filter(
        User.last_login >= thirty_days_ago
    ).scalar()

    # Most cooked recipes (top 10)
    most_cooked = db.query(
        Recipe.id,
        Recipe.title,
        Recipe.times_cooked
    ).filter(
        Recipe.is_deleted == False,
        Recipe.times_cooked > 0
    ).order_by(
        Recipe.times_cooked.desc()
    ).limit(10).all()

    most_cooked_list = [
        {
            "recipe_id": str(r.id),
            "title": r.title,
            "times_cooked": r.times_cooked
        }
        for r in most_cooked
    ]

    # Most favorited recipes (by average rating, top 10)
    most_favorited = db.query(
        Recipe.id,
        Recipe.title,
        func.avg(Rating.rating).label('avg_rating'),
        func.count(Rating.id).label('rating_count')
    ).join(
        Rating, Recipe.id == Rating.recipe_id
    ).filter(
        Recipe.is_deleted == False
    ).group_by(
        Recipe.id, Recipe.title
    ).order_by(
        func.avg(Rating.rating).desc(),
        func.count(Rating.id).desc()
    ).limit(10).all()

    most_favorited_list = [
        {
            "recipe_id": str(r.id),
            "title": r.title,
            "avg_rating": float(r.avg_rating) if r.avg_rating else 0,
            "rating_count": r.rating_count
        }
        for r in most_favorited
    ]

    # Recipe difficulty distribution
    difficulty_dist = db.query(
        Recipe.difficulty,
        func.count(Recipe.id).label('count')
    ).filter(
        Recipe.is_deleted == False,
        Recipe.difficulty.isnot(None)
    ).group_by(
        Recipe.difficulty
    ).all()

    difficulty_distribution = {
        d.difficulty: d.count for d in difficulty_dist
    }

    # Recipes created over time (last 12 months)
    twelve_months_ago = datetime.now() - timedelta(days=365)
    recipes_by_month = db.query(
        func.date_trunc('month', Recipe.created_at).label('month'),
        func.count(Recipe.id).label('count')
    ).filter(
        Recipe.created_at >= twelve_months_ago,
        Recipe.is_deleted == False
    ).group_by(
        func.date_trunc('month', Recipe.created_at)
    ).order_by(
        func.date_trunc('month', Recipe.created_at)
    ).all()

    recipes_over_time = [
        {
            "month": r.month.isoformat() if r.month else None,
            "count": r.count
        }
        for r in recipes_by_month
    ]

    # Total inventory value (if unit prices were tracked - simplified here)
    low_stock_count = db.query(func.count(InventoryItem.id)).filter(
        InventoryItem.quantity <= InventoryItem.threshold
    ).scalar()

    return {
        "totals": {
            "users": total_users,
            "recipes": total_recipes,
            "menu_plans": total_menu_plans,
            "inventory_items": total_inventory_items,
            "active_users": active_users,
            "low_stock_items": low_stock_count
        },
        "most_cooked_recipes": most_cooked_list,
        "most_favorited_recipes": most_favorited_list,
        "difficulty_distribution": difficulty_distribution,
        "recipes_over_time": recipes_over_time,
        "generated_at": datetime.now().isoformat()
    }

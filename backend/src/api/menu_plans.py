"""Menu Planning API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import date

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.user import User
from src.schemas.menu_plan import MenuPlanCreate, MenuPlanUpdate, MenuPlanResponse
from src.services.menu_plan_service import MenuPlanService

router = APIRouter()

@router.get("", response_model=dict)
async def list_menu_plans(week_start: Optional[date] = None, active_only: bool = True, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plans = MenuPlanService.list_menu_plans(db, week_start, active_only)
    return {"menu_plans": [MenuPlanResponse.model_validate(p) for p in plans]}

@router.post("", response_model=MenuPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_menu_plan(plan_data: MenuPlanCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return MenuPlanService.create_menu_plan(db, plan_data, current_user.id)

@router.get("/{planId}", response_model=MenuPlanResponse)
async def get_menu_plan(planId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = MenuPlanService.get_menu_plan(db, planId)
    if not plan: raise HTTPException(status_code=404, detail="Menu plan not found")
    return plan

@router.put("/{planId}", response_model=MenuPlanResponse)
async def update_menu_plan(planId: UUID, plan_data: MenuPlanUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = MenuPlanService.update_menu_plan(db, planId, plan_data)
    if not plan: raise HTTPException(status_code=404, detail="Menu plan not found")
    return plan

@router.delete("/{planId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_plan(planId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not MenuPlanService.delete_menu_plan(db, planId): raise HTTPException(status_code=404, detail="Menu plan not found")

@router.post("/{planId}/meals/{mealId}/cooked", response_model=dict)
async def mark_meal_cooked(planId: UUID, mealId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meal, changes = MenuPlanService.mark_meal_cooked(db, planId, mealId, current_user.id)
    if not meal: raise HTTPException(status_code=404, detail="Meal not found")
    return {"meal": meal, "inventory_changes": changes}

@router.post("/{planId}/copy", response_model=MenuPlanResponse)
async def copy_menu_plan(
    planId: UUID,
    copy_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Copy an existing menu plan to a new week.

    Args:
        planId: Source plan ID to copy
        copy_data: Must contain 'week_start_date' (ISO format)

    Returns:
        New menu plan with copied meals
    """
    week_start_str = copy_data.get("week_start_date")
    if not week_start_str:
        raise HTTPException(status_code=400, detail="week_start_date required")

    try:
        week_start = date.fromisoformat(week_start_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    new_plan = MenuPlanService.copy_menu_plan(db, planId, week_start, current_user.id)
    if not new_plan:
        raise HTTPException(status_code=404, detail="Source menu plan not found")

    return new_plan

@router.post("/suggest", response_model=MenuPlanResponse)
async def suggest_week_plan(
    week_start: date = Query(..., description="Start date for the week (YYYY-MM-DD)"),
    strategy: str = Query("rotation", description="Suggestion strategy: rotation, favorites, available_inventory"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Auto-generate a week plan using recipe suggestions.

    Creates a complete week plan with variety (no recipe repeated in same week).

    Args:
        week_start: Start date for the week
        strategy: Recipe suggestion strategy to use

    Returns:
        Generated menu plan with meals
    """
    plan = MenuPlanService.suggest_week_plan(db, week_start, current_user.id, strategy)
    return plan

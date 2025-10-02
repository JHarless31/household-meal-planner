"""
Menu Plan Schemas
Pydantic models for menu planning operations
"""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.schemas.recipe import RecipeSummary


class PlannedMealInput(BaseModel):
    """Schema for creating/updating planned meals"""

    recipe_id: UUID = Field(..., description="Recipe to plan")
    meal_date: date = Field(..., description="Date of meal")
    meal_type: str = Field(
        ..., description="Meal type (breakfast, lunch, dinner, snack)"
    )
    servings_planned: Optional[int] = Field(
        None, gt=0, description="Number of servings"
    )
    notes: Optional[str] = Field(None, description="Meal notes")

    @field_validator("meal_type")
    @classmethod
    def validate_meal_type(cls, v):
        if v not in ["breakfast", "lunch", "dinner", "snack"]:
            raise ValueError("Meal type must be breakfast, lunch, dinner, or snack")
        return v


class PlannedMealResponse(BaseModel):
    """Schema for planned meal response"""

    id: UUID
    recipe: RecipeSummary
    meal_date: date
    meal_type: str
    servings_planned: Optional[int] = None
    notes: Optional[str] = None
    cooked: bool
    cooked_date: Optional[datetime] = None
    cooked_by: Optional[UUID] = None

    class Config:
        from_attributes = True


class MenuPlanCreate(BaseModel):
    """Schema for creating a menu plan"""

    week_start_date: date = Field(..., description="Monday of the week")
    name: Optional[str] = Field(None, max_length=100, description="Optional plan name")

    @field_validator("week_start_date")
    @classmethod
    def validate_week_start(cls, v):
        if v.weekday() != 0:  # 0 is Monday
            raise ValueError("week_start_date must be a Monday")
        return v


class MenuPlanUpdate(BaseModel):
    """Schema for updating a menu plan"""

    name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    meals: Optional[List[PlannedMealInput]] = None


class MenuPlanResponse(BaseModel):
    """Schema for menu plan response"""

    id: UUID
    week_start_date: date
    name: Optional[str] = None
    meals: List[PlannedMealResponse]
    created_by: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

"""
Recipe Schemas
Pydantic models for recipe-related operations
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class IngredientInput(BaseModel):
    """Schema for creating/updating ingredients"""

    name: str = Field(..., description="Ingredient name")
    quantity: Optional[Decimal] = Field(None, ge=0, description="Quantity")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    category: Optional[str] = Field(None, description="Ingredient category")
    is_optional: Optional[bool] = Field(False, description="Optional ingredient flag")


class IngredientResponse(IngredientInput):
    """Schema for ingredient response"""

    id: UUID
    display_order: int

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    """Base recipe schema"""

    title: str = Field(..., max_length=255, description="Recipe title")
    description: Optional[str] = Field(None, description="Recipe description")
    prep_time_minutes: Optional[int] = Field(
        None, ge=0, description="Preparation time in minutes"
    )
    cook_time_minutes: Optional[int] = Field(
        None, ge=0, description="Cooking time in minutes"
    )
    servings: Optional[int] = Field(None, gt=0, description="Number of servings")
    difficulty: Optional[str] = Field(None, description="Difficulty level")
    tags: Optional[List[str]] = Field(default_factory=list, description="Recipe tags")
    source_url: Optional[str] = Field(None, description="Source URL")

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v):
        if v is not None and v not in ["easy", "medium", "hard"]:
            raise ValueError("Difficulty must be easy, medium, or hard")
        return v


class RecipeCreate(RecipeBase):
    """Schema for creating a recipe"""

    ingredients: List[IngredientInput] = Field(
        ..., min_length=1, description="Recipe ingredients"
    )
    instructions: str = Field(..., min_length=1, description="Cooking instructions")


class RecipeUpdate(RecipeCreate):
    """Schema for updating a recipe (creates new version)"""

    change_description: Optional[str] = Field(
        None, description="Description of changes"
    )


class RecipeSummary(BaseModel):
    """Schema for recipe summary (list view)"""

    id: UUID
    title: str
    description: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    is_favorite: bool = False
    last_cooked_date: Optional[date] = None

    class Config:
        from_attributes = True


class RecipeResponse(RecipeSummary):
    """Schema for detailed recipe response"""

    source_url: Optional[str] = None
    source_type: str
    current_version: int
    ingredients: List[IngredientResponse]
    instructions: str
    images: List[str] = Field(default_factory=list)
    nutritional_info: Optional[Dict[str, Any]] = None
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class RecipeVersionResponse(BaseModel):
    """Schema for recipe version response"""

    version_number: int
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    ingredients: List[IngredientResponse]
    instructions: str
    change_description: Optional[str] = None
    modified_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ScrapedRecipeResponse(BaseModel):
    """Schema for scraped recipe response"""

    scraped_data: RecipeCreate
    source_url: str
    warnings: List[str] = Field(default_factory=list)

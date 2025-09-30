"""
Shopping List Schemas
Pydantic models for shopping list operations
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class ShoppingListItem(BaseModel):
    """Schema for shopping list item"""
    id: UUID
    name: str = Field(..., description="Item name")
    quantity: Decimal = Field(..., description="Required quantity")
    unit: str = Field(..., description="Unit of measurement")
    category: str = Field(..., description="Item category")
    needed_for_recipes: List[str] = Field(default_factory=list, description="Recipe titles needing this ingredient")
    in_stock: bool = Field(..., description="Whether item is in stock")
    checked: bool = Field(False, description="Whether item has been purchased")


class ShoppingListResponse(BaseModel):
    """Schema for shopping list response"""
    menu_plan_id: UUID
    items: List[ShoppingListItem]
    generated_at: datetime

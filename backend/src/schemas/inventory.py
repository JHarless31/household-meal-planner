"""
Inventory Schemas
Pydantic models for inventory-related operations
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class InventoryItemBase(BaseModel):
    """Base inventory item schema"""

    item_name: str = Field(..., max_length=255, description="Item name")
    quantity: Decimal = Field(..., ge=0, description="Current quantity")
    unit: Optional[str] = Field(None, max_length=50, description="Unit of measurement")
    category: Optional[str] = Field(None, max_length=50, description="Item category")
    location: Optional[str] = Field(None, description="Storage location")
    expiration_date: Optional[date] = Field(None, description="Expiration date")
    minimum_stock: Optional[Decimal] = Field(0, ge=0, description="Minimum stock level")
    notes: Optional[str] = Field(None, description="Additional notes")

    @field_validator("location")
    @classmethod
    def validate_location(cls, v):
        if v is not None and v not in ["pantry", "fridge", "freezer", "other"]:
            raise ValueError("Location must be pantry, fridge, freezer, or other")
        return v


class InventoryItemCreate(InventoryItemBase):
    """Schema for creating inventory item"""

    pass


class InventoryItemUpdate(BaseModel):
    """Schema for updating inventory item"""

    item_name: Optional[str] = Field(None, max_length=255)
    quantity: Optional[Decimal] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = None
    expiration_date: Optional[date] = None
    minimum_stock: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None

    @field_validator("location")
    @classmethod
    def validate_location(cls, v):
        if v is not None and v not in ["pantry", "fridge", "freezer", "other"]:
            raise ValueError("Location must be pantry, fridge, freezer, or other")
        return v


class InventoryItemResponse(InventoryItemBase):
    """Schema for inventory item response"""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InventoryHistoryResponse(BaseModel):
    """Schema for inventory history response"""

    id: UUID
    change_type: str
    quantity_before: Decimal
    quantity_after: Decimal
    reason: Optional[str] = None
    changed_by: Optional[UUID] = None
    changed_at: datetime

    class Config:
        from_attributes = True

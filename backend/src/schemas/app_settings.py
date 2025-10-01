"""
App Settings Schemas
Pydantic models for application settings
"""

from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class AppSettingsResponse(BaseModel):
    """Schema for app settings response"""
    favorites_threshold: Decimal = Field(..., ge=0, le=1, description="Percentage of thumbs up required for favorite")
    favorites_min_raters: int = Field(..., gt=0, description="Minimum number of raters required")
    rotation_period_days: int = Field(..., gt=0, description="Days before recipe considered not recently cooked")
    low_stock_threshold_percent: Decimal = Field(..., ge=0, le=1, description="Percentage of minimum stock for low stock alert")
    expiration_warning_days: int = Field(..., ge=0, description="Days before expiration to show warning")
    updated_at: datetime

    class Config:
        from_attributes = True


class AppSettingsUpdate(BaseModel):
    """Schema for updating app settings"""
    favorites_threshold: Decimal = Field(..., ge=0, le=1)
    favorites_min_raters: int = Field(..., gt=0)
    rotation_period_days: int = Field(..., gt=0)
    low_stock_threshold_percent: Decimal = Field(..., ge=0, le=1)
    expiration_warning_days: int = Field(..., ge=0)

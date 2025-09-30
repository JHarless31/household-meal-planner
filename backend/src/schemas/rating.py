"""
Rating Schemas
Pydantic models for rating-related operations
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class RatingBase(BaseModel):
    """Base rating schema"""
    rating: bool = Field(..., description="True for thumbs up, False for thumbs down")
    feedback: Optional[str] = Field(None, description="User feedback")
    modifications: Optional[str] = Field(None, description="Suggested modifications")


class RatingCreate(RatingBase):
    """Schema for creating/updating a rating"""
    pass


class RatingResponse(RatingBase):
    """Schema for rating response"""
    id: UUID
    recipe_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RatingSummaryResponse(BaseModel):
    """Schema for rating summary"""
    recipe_id: UUID
    thumbs_up_count: int
    thumbs_down_count: int
    total_ratings: int
    is_favorite: bool

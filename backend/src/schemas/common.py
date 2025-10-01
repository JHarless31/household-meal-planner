"""
Common Schemas
Shared Pydantic models used across the API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class PaginationResponse(BaseModel):
    """Pagination metadata for list responses"""
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    total_items: int = Field(..., description="Total number of items")


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class MessageResponse(BaseModel):
    """Simple message response"""
    message: str = Field(..., description="Response message")

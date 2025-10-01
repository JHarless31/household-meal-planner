"""
User Schemas
Pydantic models for user-related operations
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    role: Optional[str] = Field("user", description="User role (admin, user, child)")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ['admin', 'user', 'child']:
            raise ValueError('Role must be admin, user, or child')
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v is not None and v not in ['admin', 'user', 'child']:
            raise ValueError('Role must be admin, user, or child')
        return v


class UserResponse(BaseModel):
    """Schema for user response"""
    id: UUID
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

"""
Pydantic validation schemas for User API requests and responses
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr = Field(..., description="User email address (must be valid)")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets minimum security requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    email: Optional[EmailStr] = Field(None, description="New email address")
    current_password: Optional[str] = Field(None, description="Current password (required for password change)")
    new_password: Optional[str] = Field(None, min_length=8, description="New password (minimum 8 characters)")

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: Optional[str]) -> Optional[str]:
        """Validate new password if provided."""
        if v is not None and len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        return v


class UserResponse(BaseModel):
    """Schema for user API responses."""
    id: int
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2


class UserLogin(BaseModel):
    """Schema for user login requests."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

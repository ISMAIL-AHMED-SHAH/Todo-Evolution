"""
Pydantic validation schemas for Task API requests and responses
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=500, description="Task title (required)")
    description: Optional[str] = Field(None, max_length=2000, description="Task description (optional)")
    priority: str = Field(default="Medium", description="Priority level: High, Medium, or Low")
    category: List[str] = Field(default_factory=list, description="Category tags for the task")
    due_date: Optional[date] = Field(None, description="Due date in ISO format (YYYY-MM-DD)")

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: str) -> str:
        """Validate priority is one of the allowed values."""
        if v not in ['High', 'Medium', 'Low']:
            raise ValueError('Priority must be High, Medium, or Low')
        return v

    @field_validator('category')
    @classmethod
    def validate_category(cls, v: List[str]) -> List[str]:
        """Validate category array constraints."""
        if len(v) > 10:
            raise ValueError('Maximum 10 categories allowed')
        for cat in v:
            if len(cat) > 50:
                raise ValueError('Category name must be 50 characters or less')
        return v


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[str] = None
    category: Optional[List[str]] = None
    due_date: Optional[date] = None
    completed: Optional[bool] = None

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        """Validate priority if provided."""
        if v is not None and v not in ['High', 'Medium', 'Low']:
            raise ValueError('Priority must be High, Medium, or Low')
        return v

    @field_validator('category')
    @classmethod
    def validate_category(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate category array if provided."""
        if v is not None:
            if len(v) > 10:
                raise ValueError('Maximum 10 categories allowed')
            for cat in v:
                if len(cat) > 50:
                    raise ValueError('Category name must be 50 characters or less')
        return v


class TaskResponse(BaseModel):
    """Schema for task API responses."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    priority: str
    category: List[str]
    due_date: Optional[date]
    completed: bool
    created_at: datetime
    updated_at: datetime
    # Computed fields
    is_overdue: bool
    days_until_due: Optional[int]

    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2


class TaskCompletionUpdate(BaseModel):
    """Schema for toggling task completion status."""
    completed: bool

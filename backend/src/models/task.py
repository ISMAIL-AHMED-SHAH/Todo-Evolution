"""
Task model for the Todo application
"""
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from .user import User


class PriorityLevel(str, Enum):
    """Priority levels for tasks."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    # Phase 2 fields
    priority: str = Field(default=PriorityLevel.MEDIUM.value, nullable=False)
    category: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    due_date: Optional[date] = None


class Task(TaskBase, table=True):
    __tablename__ = "task"
    __table_args__ = {'extend_existing': True}

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    title: str = Field(nullable=False, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, index=True)
    # Phase 2 fields
    priority: str = Field(default=PriorityLevel.MEDIUM.value, nullable=False)
    category: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    due_date: Optional[date] = Field(default=None, index=True)
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")

    def is_overdue(self) -> bool:
        """Check if task is overdue (has due_date in the past and not completed)."""
        if self.due_date is None or self.completed:
            return False
        return self.due_date < date.today()

    def days_until_due(self) -> Optional[int]:
        """Calculate days until due date (negative if overdue)."""
        if self.due_date is None:
            return None
        delta = self.due_date - date.today()
        return delta.days


class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    # Computed fields
    is_overdue: bool = False
    days_until_due: Optional[int] = None


class TaskCreate(TaskBase):
    title: str  # Title is required for creation


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    category: Optional[List[str]] = None
    due_date: Optional[date] = None


class TaskCompletionUpdate(SQLModel):
    completed: bool
"""
User model for the Todo application
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Integer, DateTime


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id: int = Field(primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255, index=True)
    # CRITICAL: Explicitly set sa_column_kwargs to ensure column name matches
    # SQLModel uses the Python field name as the database column name by default
    password_hash: str = Field(
        nullable=False,
        max_length=255,
        sa_column_kwargs={"name": "password_hash"}  # Explicit column name
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"name": "created_at"}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"name": "updated_at"}
    )

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    email: str
    password: str  # Plain text password that will be hashed


class UserUpdate(SQLModel):
    email: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
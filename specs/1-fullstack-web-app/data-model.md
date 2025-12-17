# Data Model: Full-Stack Todo Web Application

**Date**: 2025-12-08
**Feature**: 1-fullstack-web-app
**Status**: Completed

## Entities

### User Entity
**Description**: Represents a registered user in the system with authentication details

**Fields**:
- `id` (integer, primary key, auto-increment)
- `email` (string, unique, not null, max length 255)
- `password_hash` (string, not null, max length 255)
- `created_at` (datetime, not null, default now)
- `updated_at` (datetime, not null, default now)

**Relationships**:
- One-to-many with Task (one user has many tasks)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet security requirements (handled by Better Auth)

**State Transitions**:
- New user registration → Active account
- Account deletion → Deleted (subject to retention policy)

### Task Entity
**Description**: Represents a todo item with user ownership and completion status

**Fields**:
- `id` (integer, primary key, auto-increment)
- `user_id` (integer, foreign key to User.id, not null)
- `title` (string, not null, max length 500)
- `description` (string, nullable, max length 2000)
- `completed` (boolean, not null, default false)
- `created_at` (datetime, not null, default now)
- `updated_at` (datetime, not null, default now)

**Relationships**:
- Many-to-one with User (many tasks belong to one user)

**Validation Rules**:
- Title must not be empty
- User_id must reference an existing user
- Completed status must be boolean value

**State Transitions**:
- Created → Active task
- Toggled → Completed/Incomplete
- Deleted → Removed from system

## Entity Relationships

### User → Task (One-to-Many)
- One user can own multiple tasks
- Each task belongs to exactly one user
- Tasks are isolated by user_id (multi-user isolation)

**Constraints**:
- Foreign key constraint on Task.user_id → User.id
- Cascade operations: When user is deleted, their tasks should be handled according to retention policy
- All queries must filter by user_id to enforce isolation

## Database Schema

### Tables

#### users table
```
id: INTEGER (PRIMARY KEY, AUTOINCREMENT)
email: VARCHAR(255) (UNIQUE, NOT NULL)
password_hash: VARCHAR(255) (NOT NULL)
created_at: TIMESTAMP (NOT NULL, DEFAULT NOW)
updated_at: TIMESTAMP (NOT NULL, DEFAULT NOW)
```

#### tasks table
```
id: INTEGER (PRIMARY KEY, AUTOINCREMENT)
user_id: INTEGER (NOT NULL, FOREIGN KEY REFERENCES users(id))
title: VARCHAR(500) (NOT NULL)
description: TEXT (NULLABLE)
completed: BOOLEAN (NOT NULL, DEFAULT FALSE)
created_at: TIMESTAMP (NOT NULL, DEFAULT NOW)
updated_at: TIMESTAMP (NOT NULL, DEFAULT NOW)
```

## Indexes

### Required Indexes
1. `users.email` - UNIQUE INDEX for efficient lookup and uniqueness constraint
2. `tasks.user_id` - INDEX for efficient querying of user-specific tasks
3. `tasks.user_id + tasks.completed` - COMPOSITE INDEX for common filtered queries

## Access Patterns

### Common Queries
1. Get all tasks for a specific user (filtered by user_id)
2. Get a specific task for a user (filtered by user_id and task_id)
3. Update task status for a specific user's task
4. Create new task for a specific user
5. Delete a specific user's task

### Security Requirements
- All queries must filter by user_id to enforce multi-user isolation
- No query should return tasks that don't belong to the authenticated user
- Authentication must be validated before any data access

## SQLModel Implementation

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False)  # Managed by Better Auth
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    title: str = Field(nullable=False, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")
```

## Validation Requirements

### Input Validation
- User email: Must pass email format validation
- Task title: Must be non-empty string with max length
- Task description: Optional, with max length limit
- User_id: Must reference existing user

### Business Logic Validation
- Users can only access their own tasks
- Task operations require valid authentication
- Task creation requires non-empty title
- Task updates require valid user ownership

## Data Integrity

### Constraints
- Referential integrity through foreign key relationships
- Unique constraints on user email
- NOT NULL constraints on required fields
- Proper indexing for performance

### Data Consistency
- Automatic timestamp updates using database defaults
- Transactional operations for data consistency
- Proper error handling for constraint violations
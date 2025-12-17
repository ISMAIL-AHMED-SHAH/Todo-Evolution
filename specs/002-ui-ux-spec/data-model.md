# Data Model: Todo App UI/UX - Phase 2 Enhancements

**Date**: 2025-12-13
**Feature**: 002-ui-ux-spec
**Status**: Planning
**Base Model**: [specs/1-fullstack-web-app/data-model.md](../1-fullstack-web-app/data-model.md)

## Overview

Phase 2 extends the existing data model with UI/UX enhancements to support richer task management features: priority levels, category tagging, and due dates with overdue detection.

## Phase 2 Enhancements

### Task Entity (Extended)

**New Fields**:
- `priority` (enum: 'High' | 'Medium' | 'Low', default 'Medium')
- `category` (JSON array of strings, default [])
- `due_date` (date, nullable)

**Complete Phase 2 Schema**:
```python
from sqlmodel import SQLModel, Field, Column, JSON
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

class PriorityLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    # Existing fields (Phase 1)
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(nullable=False, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Phase 2 enhancements
    priority: str = Field(default=PriorityLevel.MEDIUM, nullable=False)
    category: List[str] = Field(default=[], sa_column=Column(JSON))
    due_date: Optional[date] = Field(default=None, index=True)

    # Relationship (existing)
    user: "User" = Relationship(back_populates="tasks")
```

### User Entity (No Changes)

The User entity remains unchanged from Phase 1. See [base data model](../1-fullstack-web-app/data-model.md#user-entity) for details.

## Validation Rules

### Priority Validation
- Must be one of: 'High', 'Medium', 'Low'
- Defaults to 'Medium' if not specified
- Used for UI color-coding:
  - High: Red badge (`bg-red-200`)
  - Medium: Orange badge (`bg-orange-200`)
  - Low: Green badge (`bg-green-200`)

### Category Validation
- Must be a JSON array of strings
- Each category tag: max 50 characters
- Maximum 10 categories per task
- Categories are case-sensitive
- Empty array is valid (no categories)

### Due Date Validation
- Must be a valid date (no time component)
- Can be null (no due date)
- Can be in the past (triggers overdue status)
- Date format: ISO 8601 (YYYY-MM-DD)

## Computed Fields (Application Layer)

### Overdue Status
**Not stored in database** - computed in application layer:
```python
def is_overdue(self) -> bool:
    """Check if task is overdue (has due_date in the past and not completed)"""
    if self.due_date is None or self.completed:
        return False
    return self.due_date < date.today()
```

### Days Until Due
```python
def days_until_due(self) -> Optional[int]:
    """Calculate days until due date (negative if overdue)"""
    if self.due_date is None:
        return None
    delta = self.due_date - date.today()
    return delta.days
```

## Database Migration (Alembic)

### Migration Script: Add Phase 2 Fields

```python
"""Add Phase 2 task fields (priority, category, due_date)

Revision ID: 002_phase2_task_fields
Revises: 001_initial_schema
Create Date: 2025-12-13
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

def upgrade():
    # Add priority column with default 'Medium'
    op.add_column('tasks',
        sa.Column('priority', sa.String(10),
                  nullable=False,
                  server_default='Medium'))

    # Add category column (JSON array)
    op.add_column('tasks',
        sa.Column('category', JSON,
                  nullable=False,
                  server_default='[]'))

    # Add due_date column (nullable)
    op.add_column('tasks',
        sa.Column('due_date', sa.Date, nullable=True))

    # Create index on due_date for efficient overdue queries
    op.create_index('ix_tasks_due_date', 'tasks', ['due_date'])

def downgrade():
    op.drop_index('ix_tasks_due_date', table_name='tasks')
    op.drop_column('tasks', 'due_date')
    op.drop_column('tasks', 'category')
    op.drop_column('tasks', 'priority')
```

## Indexes

### Existing Indexes (Phase 1)
1. `tasks.user_id` - For user-specific task queries
2. `tasks(user_id, completed)` - Composite for filtered queries

### New Indexes (Phase 2)
3. `tasks.due_date` - For overdue task queries and sorting by due date
4. `tasks(user_id, priority)` - Composite for priority-filtered queries (optional, add if needed)

**Index Strategy**:
- Keep indexes minimal to balance query performance vs write overhead
- Monitor query patterns and add indexes as needed
- Consider `tasks(user_id, due_date, completed)` if overdue queries are frequent

## Updated Access Patterns

### Common Queries (Phase 2)

1. **Get all tasks with filters**:
   ```sql
   SELECT * FROM tasks
   WHERE user_id = ?
     AND (completed = ? OR ? IS NULL)
     AND (priority = ? OR ? IS NULL)
   ORDER BY due_date ASC NULLS LAST, created_at DESC
   ```

2. **Get overdue tasks**:
   ```sql
   SELECT * FROM tasks
   WHERE user_id = ?
     AND completed = FALSE
     AND due_date < CURRENT_DATE
   ORDER BY due_date ASC
   ```

3. **Get tasks by category** (JSON array search):
   ```sql
   SELECT * FROM tasks
   WHERE user_id = ?
     AND category @> ?::jsonb  -- PostgreSQL JSONB contains operator
   ```

4. **Task statistics** (for dashboard):
   ```sql
   SELECT
     COUNT(*) FILTER (WHERE completed = TRUE) as completed_count,
     COUNT(*) FILTER (WHERE completed = FALSE) as pending_count,
     COUNT(*) FILTER (WHERE completed = FALSE AND due_date < CURRENT_DATE) as overdue_count,
     COUNT(*) FILTER (WHERE priority = 'High') as high_priority_count
   FROM tasks
   WHERE user_id = ?
   ```

## API Request/Response Models

### Task Input (Create/Update)

```typescript
// Frontend TypeScript types
interface CreateTaskInput {
  title: string;                    // Required, max 500 chars
  description?: string;              // Optional, max 2000 chars
  priority?: 'High' | 'Medium' | 'Low';  // Optional, defaults to 'Medium'
  category?: string[];               // Optional, defaults to []
  due_date?: string;                 // Optional, ISO date format (YYYY-MM-DD)
}

interface UpdateTaskInput {
  title?: string;
  description?: string | null;
  priority?: 'High' | 'Medium' | 'Low';
  category?: string[];
  due_date?: string | null;
  completed?: boolean;
}
```

### Task Output (Response)

```typescript
interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  priority: 'High' | 'Medium' | 'Low';
  category: string[];
  due_date: string | null;          // ISO date format (YYYY-MM-DD)
  completed: boolean;
  created_at: string;                // ISO datetime
  updated_at: string;                // ISO datetime

  // Computed fields (not in database)
  is_overdue?: boolean;              // Computed on backend
  days_until_due?: number | null;    // Computed on backend
}
```

### Backend Pydantic Models

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    priority: str = Field(default="Medium")
    category: List[str] = Field(default_factory=list)
    due_date: Optional[date] = None

    @validator('priority')
    def validate_priority(cls, v):
        if v not in ['High', 'Medium', 'Low']:
            raise ValueError('Priority must be High, Medium, or Low')
        return v

    @validator('category')
    def validate_category(cls, v):
        if len(v) > 10:
            raise ValueError('Maximum 10 categories allowed')
        for cat in v:
            if len(cat) > 50:
                raise ValueError('Category name must be 50 characters or less')
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[str] = None
    category: Optional[List[str]] = None
    due_date: Optional[date] = None
    completed: Optional[bool] = None

    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ['High', 'Medium', 'Low']:
            raise ValueError('Priority must be High, Medium, or Low')
        return v

class TaskResponse(BaseModel):
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
        orm_mode = True
```

## Data Integrity & Constraints

### Database Constraints
- `priority` NOT NULL with CHECK constraint: `priority IN ('High', 'Medium', 'Low')`
- `category` NOT NULL with default `'[]'::jsonb`
- `due_date` nullable, no constraint
- Foreign key: `user_id` → `users.id` with ON DELETE CASCADE

### Application-Level Validation
- Priority enum validation in Pydantic models
- Category array length and string length validation
- Due date format validation (ISO 8601)
- User ownership verification (existing from Phase 1)

## Performance Considerations

### Index Usage
- `due_date` index for overdue queries: ~5-10ms for 10k tasks
- Composite `(user_id, due_date, completed)` if overdue queries are frequent
- JSON category searching: Use PostgreSQL JSONB with GIN index if category filtering becomes common

### Query Optimization
- Overdue tasks computed efficiently with index on `due_date`
- Statistics query uses single scan with COUNT FILTER
- Consider caching dashboard statistics in Redis if >100k tasks per user

### Storage
- JSON category field: ~50-200 bytes per task (varies with tag count)
- Due date: 4 bytes (PostgreSQL DATE type)
- Priority: ~10 bytes (stored as VARCHAR)
- **Total additional storage**: ~100-250 bytes per task

## Security Considerations

### Input Sanitization
- Escape category strings to prevent XSS (handled by frontend framework)
- Validate due_date format to prevent SQL injection (use parameterized queries)
- Priority enum prevents invalid values

### Access Control
- All queries must filter by `user_id` (existing from Phase 1)
- No new security concerns introduced by Phase 2 fields
- Category field does not contain sensitive data (user-defined tags)

## Testing Requirements

### Database Tests
- ✅ Migration applies successfully
- ✅ Default values work correctly (priority='Medium', category=[])
- ✅ NULL due_date is allowed
- ✅ Priority CHECK constraint rejects invalid values
- ✅ Category JSON array serialization/deserialization

### Application Tests
- ✅ Overdue detection works correctly (boundary cases: today, yesterday, tomorrow)
- ✅ Days until due calculation (positive, negative, null)
- ✅ Priority badge color mapping
- ✅ Category tag validation (length, count)
- ✅ Due date parsing from ISO string

### API Tests
- ✅ Create task with all Phase 2 fields
- ✅ Update task priority, category, due_date
- ✅ Filter tasks by priority
- ✅ Get overdue tasks only
- ✅ Dashboard statistics include Phase 2 data

## Migration Rollout Plan

### Step 1: Database Migration
1. Run Alembic migration on staging environment
2. Verify existing tasks have default values (priority='Medium', category=[])
3. Test rollback procedure
4. Run migration on production during low-traffic window

### Step 2: Backend Deployment
1. Deploy updated SQLModel models
2. Deploy updated Pydantic validation models
3. Deploy updated API endpoints (backward compatible - new fields optional)
4. Verify existing API contracts still work

### Step 3: Frontend Deployment
1. Deploy UI components for priority badges, category tags, due date picker
2. Update task forms with new fields (all optional)
3. Enable Phase 2 features with feature flag
4. Monitor for errors and rollback if needed

### Step 4: Validation
1. Create test tasks with Phase 2 fields
2. Verify overdue detection
3. Verify priority filtering
4. Verify category search
5. Monitor database performance (query times, index usage)

---

**Migration Status**: Pending
**Backward Compatibility**: ✅ Yes (all Phase 2 fields are optional or have defaults)
**Database Impact**: Low (adds 3 columns, 1 index)
**Estimated Downtime**: < 5 minutes (for migration only)

# Database Specification: SQLModel Schemas for User and Task

**Database**: PostgreSQL Schema | **Created**: 2025-12-08 | **Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Account Storage (Priority: P1)

As a system designer, I want to store user account information in the database so that authentication and user isolation can be properly implemented.

**Why this priority**: This is foundational for the multi-user system.

**Independent Test**: User account data can be stored, retrieved, updated, and deleted properly.

**Acceptance Scenarios**:

1. **Given** a new user signing up, **When** their account is created, **Then** their user data should be stored in the database with proper constraints.
2. **Given** an existing user, **When** their account information is accessed, **Then** the data should be retrieved accurately and efficiently.
3. **Given** a user updating their account, **When** changes are saved, **Then** the database should reflect the updated information.

---

### User Story 2 - Task Storage and Retrieval (Priority: P1)

As a system designer, I want to store tasks in the database with proper relationships to users so that each user has their own isolated task list.

**Why this priority**: This is the core data model for the todo application.

**Independent Test**: Task data can be stored, retrieved, updated, and deleted with proper user ownership.

**Acceptance Scenarios**:

1. **Given** a user creating a task, **When** the task is saved, **Then** it should be stored in the database with proper user association.
2. **Given** a user accessing their tasks, **When** the data is retrieved, **Then** only their tasks should be returned, not others'.
3. **Given** a user updating a task, **When** changes are saved, **Then** the database should reflect the updated information with proper timestamps.

---

### User Story 3 - Data Integrity and Constraints (Priority: P1)

As a system designer, I want to enforce data integrity through database constraints so that the application maintains consistent and valid data.

**Why this priority**: This prevents data corruption and ensures application reliability.

**Independent Test**: Invalid data cannot be inserted into the database due to proper constraints.

**Acceptance Scenarios**:

1. **Given** an attempt to insert a task with a null title, **When** the database operation occurs, **Then** it should fail due to NOT NULL constraint.
2. **Given** an attempt to insert a task with an invalid user_id, **When** the database operation occurs, **Then** it should fail due to foreign key constraint.
3. **Given** a valid task update operation, **When** it occurs, **Then** the updated_at timestamp should be automatically updated.

---

### Edge Cases

- What happens when the database is full or unavailable? (Should have appropriate error handling)
- How does the system handle concurrent access to the same data? (Should handle with proper transactions)
- What happens when referential integrity is violated? (Should enforce constraints)
- How does the system handle very large text fields? (Should have appropriate size limits)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Database MUST store User entities with email, password hash, and account metadata
- **FR-002**: Database MUST store Task entities with id, user_id, title, description, completed status, created_at, updated_at
- **FR-003**: Database MUST enforce NOT NULL constraint on critical fields like title and user_id
- **FR-004**: Database MUST enforce foreign key relationship between Task.user_id and User.id
- **FR-005**: Database MUST automatically manage created_at and updated_at timestamps for tasks
- **FR-006**: Database MUST ensure unique email addresses for User entities
- **FR-007**: Database MUST support efficient querying of tasks by user_id
- **FR-008**: Database MUST maintain data consistency during concurrent operations
- **FR-009**: Database MUST support proper indexing for frequently queried fields

### Key Entities *(include if feature involves data)*

- **User**: Entity representing a registered user with authentication details, referenced from Better Auth
  - Fields: id (primary key), email (unique, not null), password_hash, created_at, updated_at
- **Task**: Entity representing a todo item with user ownership
  - Fields: id (primary key), user_id (foreign key to User), title (not null), description, completed (boolean, default false), created_at, updated_at

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Database queries for user tasks complete within 100ms for 95% of requests
- **SC-002**: 100% of data integrity constraints are enforced preventing invalid data entry
- **SC-003**: Database maintains consistent state during concurrent operations with 99.9% success rate
- **SC-004**: User and Task entities can be created, read, updated, deleted with 99.9% success rate
- **SC-005**: Database storage efficiently supports up to 1 million tasks with acceptable performance
- **SC-006**: Foreign key relationships prevent orphaned task records with 100% enforcement
- **SC-007**: Unique constraints on email addresses prevent duplicate user accounts with 100% enforcement

## SQLModel Schema Definitions

### User Model (Referenced from Better Auth)
```python
# Note: This model is primarily managed by Better Auth
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False)  # Managed by Better Auth
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")
```

### Task Model
```python
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

### Database Constraints
- User.email: UNIQUE, NOT NULL
- Task.title: NOT NULL
- Task.user_id: FOREIGN KEY to User.id, NOT NULL
- Task.completed: BOOLEAN with default FALSE
- created_at and updated_at: TIMESTAMP with automatic defaults

### Required Indexes
- User.email: UNIQUE INDEX for efficient lookup and uniqueness
- Task.user_id: INDEX for efficient querying of user-specific tasks
- Task.user_id + Task.completed: COMPOSITE INDEX for common filtered queries
# API Contracts: Todo App UI/UX - Phase 2

**Date**: 2025-12-13
**Feature**: 002-ui-ux-spec
**Status**: Planning
**Base API**: [specs/api/rest-endpoints.md](../api/rest-endpoints.md)

## Overview

This document specifies the complete REST API contract for the Todo App Phase 2, including authentication flows, task management endpoints with Phase 2 enhancements (priority, category, due_date), and user profile endpoints.

## Authentication

### JWT Token Structure

All authenticated endpoints require an `Authorization` header with a Bearer token issued by Better Auth.

**Request Header**:
```
Authorization: Bearer <jwt_token>
```

**JWT Claims** (issued by Better Auth):
```json
{
  "sub": "user_123",           // User ID (string)
  "email": "user@example.com", // User email
  "iat": 1702468800,           // Issued at (Unix timestamp)
  "exp": 1702555200            // Expiration (Unix timestamp)
}
```

**Backend Verification**:
- Extract token from `Authorization: Bearer <token>` header
- Verify signature using `BETTER_AUTH_SECRET` environment variable
- Decode JWT to extract `user_id` from `sub` claim
- Verify `user_id` in URL path matches JWT `sub` claim
- Return 401 if token is invalid/expired
- Return 403 if user_id mismatch (authorization failure)

## Error Response Format

All error responses follow this standard format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "validation error detail"  // Optional, for validation errors
  }
}
```

**HTTP Status Codes**:
- `200 OK` - Successful GET, PUT, DELETE, PATCH
- `201 Created` - Successful POST (resource created)
- `400 Bad Request` - Invalid input, validation errors
- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - Valid JWT but user doesn't own resource
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Unexpected server error

## Task Endpoints

### GET /api/{user_id}/tasks

Retrieve all tasks for authenticated user with optional filters.

**URL Parameters**:
- `user_id` (integer, required) - User ID from JWT token

**Query Parameters** (all optional):
- `completed` (boolean) - Filter by completion status (true/false)
- `priority` (string) - Filter by priority ('High', 'Medium', 'Low')
- `overdue` (boolean) - Show only overdue tasks (due_date < today AND completed = false)
- `category` (string) - Filter tasks containing this category tag
- `sort` (string) - Sort order ('due_date_asc', 'due_date_desc', 'created_desc', 'priority')

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": 123,
      "title": "Complete project proposal",
      "description": "Draft and finalize Q1 project proposal",
      "priority": "High",
      "category": ["work", "urgent"],
      "due_date": "2025-12-20",
      "completed": false,
      "created_at": "2025-12-10T10:00:00Z",
      "updated_at": "2025-12-12T15:30:00Z",
      "is_overdue": false,
      "days_until_due": 7
    }
  ],
  "total": 1,
  "filters_applied": {
    "completed": null,
    "priority": null,
    "overdue": null,
    "category": null
  }
}
```

**Error Responses**:
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - user_id in URL doesn't match JWT user_id

---

### POST /api/{user_id}/tasks

Create a new task for authenticated user.

**URL Parameters**:
- `user_id` (integer, required)

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Complete project proposal",
  "description": "Draft and finalize Q1 project proposal",  // Optional
  "priority": "High",                                       // Optional, defaults to 'Medium'
  "category": ["work", "urgent"],                           // Optional, defaults to []
  "due_date": "2025-12-20"                                  // Optional, ISO date (YYYY-MM-DD)
}
```

**Validation Rules**:
- `title`: Required, non-empty, max 500 characters
- `description`: Optional, max 2000 characters
- `priority`: Optional, must be 'High', 'Medium', or 'Low'
- `category`: Optional, array of strings (max 10 items, each max 50 chars)
- `due_date`: Optional, valid ISO date format (YYYY-MM-DD)

**Response (201 Created)**:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Complete project proposal",
  "description": "Draft and finalize Q1 project proposal",
  "priority": "High",
  "category": ["work", "urgent"],
  "due_date": "2025-12-20",
  "completed": false,
  "created_at": "2025-12-13T10:00:00Z",
  "updated_at": "2025-12-13T10:00:00Z",
  "is_overdue": false,
  "days_until_due": 7
}
```

**Error Responses**:
- `400 Bad Request` - Validation error (missing title, invalid priority, etc.)
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - user_id mismatch

**Example Error (400)**:
```json
{
  "error": "validation_error",
  "message": "Invalid request body",
  "details": {
    "title": "Title is required",
    "priority": "Priority must be one of: High, Medium, Low"
  }
}
```

---

### GET /api/{user_id}/tasks/{id}

Retrieve a specific task by ID.

**URL Parameters**:
- `user_id` (integer, required)
- `id` (integer, required) - Task ID

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Complete project proposal",
  "description": "Draft and finalize Q1 project proposal",
  "priority": "High",
  "category": ["work", "urgent"],
  "due_date": "2025-12-20",
  "completed": false,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-12T15:30:00Z",
  "is_overdue": false,
  "days_until_due": 7
}
```

**Error Responses**:
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - Task exists but doesn't belong to user
- `404 Not Found` - Task doesn't exist

---

### PUT /api/{user_id}/tasks/{id}

Update a task (full replacement of editable fields).

**URL Parameters**:
- `user_id` (integer, required)
- `id` (integer, required) - Task ID

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body** (all fields optional):
```json
{
  "title": "Updated project proposal",
  "description": "New description",
  "priority": "Medium",
  "category": ["work", "planning"],
  "due_date": "2025-12-25",
  "completed": false
}
```

**Validation Rules**:
- If provided, fields follow same validation as POST
- Omitted fields retain their current values
- `completed` can be set to true/false

**Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Updated project proposal",
  "description": "New description",
  "priority": "Medium",
  "category": ["work", "planning"],
  "due_date": "2025-12-25",
  "completed": false,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-13T11:00:00Z",
  "is_overdue": false,
  "days_until_due": 12
}
```

**Error Responses**:
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - Task doesn't belong to user
- `404 Not Found` - Task doesn't exist

---

### PATCH /api/{user_id}/tasks/{id}/complete

Toggle task completion status (quick action).

**URL Parameters**:
- `user_id` (integer, required)
- `id` (integer, required) - Task ID

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Complete project proposal",
  "description": "Draft and finalize Q1 project proposal",
  "priority": "High",
  "category": ["work", "urgent"],
  "due_date": "2025-12-20",
  "completed": true,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-13T11:30:00Z",
  "is_overdue": false,
  "days_until_due": 7
}
```

**Error Responses**:
- `400 Bad Request` - Missing or invalid `completed` field
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - Task doesn't belong to user
- `404 Not Found` - Task doesn't exist

---

### DELETE /api/{user_id}/tasks/{id}

Delete a task permanently.

**URL Parameters**:
- `user_id` (integer, required)
- `id` (integer, required) - Task ID

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Complete project proposal",
  "description": "Draft and finalize Q1 project proposal",
  "priority": "High",
  "category": ["work", "urgent"],
  "due_date": "2025-12-20",
  "completed": false,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-12T15:30:00Z",
  "is_overdue": false,
  "days_until_due": 7,
  "deleted_at": "2025-12-13T12:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - Task doesn't belong to user
- `404 Not Found` - Task doesn't exist

---

## User Profile Endpoints (New)

### GET /api/{user_id}/profile

Retrieve user profile information.

**URL Parameters**:
- `user_id` (integer, required)

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "id": 123,
  "email": "user@example.com",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-12-13T10:00:00Z",
  "task_stats": {
    "total": 25,
    "completed": 15,
    "pending": 10,
    "overdue": 2
  }
}
```

**Error Responses**:
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - user_id doesn't match JWT user_id

---

### PUT /api/{user_id}/profile

Update user profile (currently only email).

**URL Parameters**:
- `user_id` (integer, required)

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "newemail@example.com"
}
```

**Validation Rules**:
- `email`: Must be valid email format
- `email`: Must be unique (not already used by another user)

**Response (200 OK)**:
```json
{
  "id": 123,
  "email": "newemail@example.com",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-12-13T12:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request` - Invalid email format or email already in use
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - user_id doesn't match JWT user_id

**Example Error (400)**:
```json
{
  "error": "validation_error",
  "message": "Email already in use",
  "details": {
    "email": "This email is already registered to another account"
  }
}
```

---

## Dashboard Statistics Endpoint (New)

### GET /api/{user_id}/stats

Get aggregated task statistics for dashboard display.

**URL Parameters**:
- `user_id` (integer, required)

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "total_tasks": 25,
  "completed_tasks": 15,
  "pending_tasks": 10,
  "overdue_tasks": 2,
  "by_priority": {
    "High": 5,
    "Medium": 12,
    "Low": 8
  },
  "by_category": {
    "work": 15,
    "personal": 8,
    "urgent": 6
  },
  "completion_rate": 0.60,
  "tasks_created_this_week": 3,
  "tasks_completed_this_week": 5
}
```

**Error Responses**:
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - user_id doesn't match JWT user_id

---

## Authentication Endpoints (Better Auth)

**Note**: Authentication is handled by Better Auth library, not custom endpoints. These flows are documented for reference.

### POST /api/auth/signup

Register a new user account (handled by Better Auth).

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (201 Created)**:
```json
{
  "user": {
    "id": 123,
    "email": "user@example.com"
  },
  "session": {
    "token": "jwt_token_here",
    "expiresAt": "2025-12-14T12:00:00Z"
  }
}
```

---

### POST /api/auth/signin

Sign in existing user (handled by Better Auth).

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": 123,
    "email": "user@example.com"
  },
  "session": {
    "token": "jwt_token_here",
    "expiresAt": "2025-12-14T12:00:00Z"
  }
}
```

**Error Response (401)**:
```json
{
  "error": "invalid_credentials",
  "message": "Invalid email or password"
}
```

---

### POST /api/auth/signout

Sign out current user (handled by Better Auth).

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "message": "Successfully signed out"
}
```

---

## TypeScript Type Definitions

### Task Types

```typescript
export type PriorityLevel = 'High' | 'Medium' | 'Low';

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  priority: PriorityLevel;
  category: string[];
  due_date: string | null;  // ISO date format (YYYY-MM-DD)
  completed: boolean;
  created_at: string;        // ISO datetime
  updated_at: string;        // ISO datetime
  is_overdue?: boolean;      // Computed field
  days_until_due?: number | null;  // Computed field
}

export interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: PriorityLevel;
  category?: string[];
  due_date?: string;  // ISO date format
}

export interface UpdateTaskInput {
  title?: string;
  description?: string | null;
  priority?: PriorityLevel;
  category?: string[];
  due_date?: string | null;
  completed?: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  filters_applied: {
    completed: boolean | null;
    priority: PriorityLevel | null;
    overdue: boolean | null;
    category: string | null;
  };
}
```

### User Types

```typescript
export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
  task_stats?: {
    total: number;
    completed: number;
    pending: number;
    overdue: number;
  };
}

export interface UpdateProfileInput {
  email: string;
}
```

### API Error Types

```typescript
export interface APIError {
  error: string;
  message: string;
  details?: Record<string, string>;
}
```

---

## Rate Limiting (Future Enhancement)

Not implemented in Phase 2, but recommended for production:

- **Per-user limits**: 100 requests per minute
- **Per-IP limits**: 500 requests per minute
- **Burst allowance**: 20 requests immediate burst

**Rate Limit Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1702555200
```

---

## CORS Configuration

**Development**:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
```

**Production**:
```
Access-Control-Allow-Origin: https://yourdomain.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
```

---

**Contract Version**: 2.0.0 (Phase 2)
**Last Updated**: 2025-12-13
**Backward Compatible**: Yes (Phase 2 fields are optional)

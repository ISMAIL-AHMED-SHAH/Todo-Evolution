# Todo App API Documentation

## Overview

The Todo App API is a RESTful API built with FastAPI that provides task management functionality with user authentication and isolation.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: TBD

## Authentication

All task endpoints require Bearer token authentication using JWT tokens.

### Headers

```
Authorization: Bearer <your_jwt_token>
```

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Endpoints

### Health Check

#### GET /health

Check if the API is running.

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "service": "todo-app-backend"
}
```

---

### Authentication Endpoints

(See separate authentication documentation)

---

### Task Endpoints

All task endpoints enforce user isolation - users can only access their own tasks.

#### GET /{user_id}/tasks

Get all tasks for the authenticated user.

**Authentication**: Required
**Path Parameters**:
- `user_id` (integer): User ID (must match authenticated user)

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "completed": false,
    "created_at": "2025-12-10T10:00:00Z",
    "updated_at": "2025-12-10T10:00:00Z"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User ID does not match authenticated user

---

#### POST /{user_id}/tasks

Create a new task for the authenticated user.

**Authentication**: Required
**Path Parameters**:
- `user_id` (integer): User ID (must match authenticated user)

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-10T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User ID does not match authenticated user
- `422 Validation Error`: Missing required fields or invalid data

---

#### GET /{user_id}/tasks/{id}

Get a specific task by ID.

**Authentication**: Required
**Path Parameters**:
- `user_id` (integer): User ID (must match authenticated user)
- `id` (integer): Task ID

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-10T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User ID does not match authenticated user
- `404 Not Found`: Task does not exist or does not belong to user

---

#### PUT /{user_id}/tasks/{id}

Update an existing task.

**Authentication**: Required
**Path Parameters**:
- `user_id` (integer): User ID (must match authenticated user)
- `id` (integer): Task ID

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-10T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User ID does not match authenticated user
- `404 Not Found`: Task does not exist or does not belong to user
- `422 Validation Error`: Invalid data

---

#### DELETE /{user_id}/tasks/{id}

Delete a task.

**Authentication**: Required
**Path Parameters**:
- `user_id` (integer): User ID (must match authenticated user)
- `id` (integer): Task ID

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Deleted task title",
  "description": "Deleted task description",
  "completed": false,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-10T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User ID does not match authenticated user
- `404 Not Found`: Task does not exist or does not belong to user

---

#### PATCH /{user_id}/tasks/{id}/complete

Toggle task completion status.

**Authentication**: Required
**Path Parameters**:
- `user_id` (integer): User ID (must match authenticated user)
- `id` (integer): Task ID

**Request Body**:
```json
{
  "completed": true
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "created_at": "2025-12-10T10:00:00Z",
  "updated_at": "2025-12-10T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User ID does not match authenticated user
- `404 Not Found`: Task does not exist or does not belong to user
- `422 Validation Error`: Missing required field

---

## Data Models

### Task

```typescript
{
  id: number;              // Auto-generated
  user_id: number;         // Foreign key to User
  title: string;           // Max 500 characters, required
  description: string?;    // Max 2000 characters, optional
  completed: boolean;      // Default: false
  created_at: datetime;    // ISO 8601 format
  updated_at: datetime;    // ISO 8601 format
}
```

### TaskCreate (Request)

```typescript
{
  title: string;           // Required
  description: string?;    // Optional
}
```

### TaskUpdate (Request)

```typescript
{
  title: string?;          // Optional
  description: string?;    // Optional
  completed: boolean?;     // Optional
}
```

### TaskCompletionUpdate (Request)

```typescript
{
  completed: boolean;      // Required
}
```

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

---

## Testing

Run the test suite:

```bash
cd backend
pytest tests/test_api_tasks.py -v
```

---

## Rate Limiting

Currently no rate limiting is implemented. This should be added for production use.

---

## CORS

The API allows requests from:
- `http://localhost:3000` (Next.js development)
- `http://localhost:3001`
- `http://127.0.0.1:3000`

---

## Security Considerations

1. **Authentication**: All task endpoints require valid JWT token
2. **User Isolation**: Users can only access their own tasks
3. **Input Validation**: All inputs are validated using Pydantic models
4. **SQL Injection Protection**: SQLModel protects against SQL injection
5. **HTTPS**: Use HTTPS in production (TLS/SSL)

---

## Development

### Running the Server

```bash
cd backend
uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
```

### Accessing Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Example Usage

### Using cURL

```bash
# Get all tasks
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/1/tasks

# Create a task
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Task","description":"Task description"}' \
  http://localhost:8000/1/tasks

# Update task completion
curl -X PATCH \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed":true}' \
  http://localhost:8000/1/tasks/1/complete
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000"
token = "YOUR_JWT_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# Get all tasks
response = requests.get(f"{BASE_URL}/1/tasks", headers=headers)
tasks = response.json()

# Create a task
new_task = {
    "title": "New Task",
    "description": "Task description"
}
response = requests.post(f"{BASE_URL}/1/tasks", json=new_task, headers=headers)
task = response.json()
```

---

## Support

For issues and questions, please refer to the project documentation or create an issue in the project repository.

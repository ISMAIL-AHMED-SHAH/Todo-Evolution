# API Specification: RESTful Endpoints for Task Management

**API**: Task Management API | **Created**: 2025-12-08 | **Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access User Tasks (Priority: P1)

As an authenticated user, I want to retrieve my tasks via API so that the frontend can display them.

**Why this priority**: This is the primary way users access their task data.

**Independent Test**: A user can make an authenticated API request to retrieve their tasks.

**Acceptance Scenarios**:

1. **Given** an authenticated user with valid JWT, **When** they make a GET request to /api/{user_id}/tasks, **Then** they should receive a 200 OK response with their task list.
2. **Given** an unauthenticated user, **When** they make a GET request to /api/{user_id}/tasks, **Then** they should receive a 401 Unauthorized response.
3. **Given** an authenticated user trying to access another user's tasks, **When** they make a GET request to /api/{other_user_id}/tasks, **Then** they should receive a 403 Forbidden response.

---

### User Story 2 - Create New Tasks (Priority: P1)

As an authenticated user, I want to create new tasks via API so that they can be stored persistently.

**Why this priority**: This is the primary way users add new items to their todo list.

**Independent Test**: A user can make an authenticated API request to create a new task.

**Acceptance Scenarios**:

1. **Given** an authenticated user with valid JWT, **When** they make a POST request to /api/{user_id}/tasks with valid task data, **Then** they should receive a 201 Created response with the new task details.
2. **Given** an authenticated user with invalid task data, **When** they make a POST request to /api/{user_id}/tasks, **Then** they should receive a 400 Bad Request response with validation errors.
3. **Given** an authenticated user trying to create a task for another user's ID, **When** they make a POST request to /api/{other_user_id}/tasks, **Then** the system should enforce user ownership and create the task for the authenticated user.

---

### User Story 3 - Manage Individual Tasks (Priority: P1)

As an authenticated user, I want to view, update, and delete specific tasks via API so that I can manage my todo list.

**Why this priority**: This provides full CRUD functionality for individual tasks.

**Independent Test**: A user can make authenticated API requests to manage specific tasks.

**Acceptance Scenarios**:

1. **Given** an authenticated user with valid JWT, **When** they make a GET request to /api/{user_id}/tasks/{task_id}, **Then** they should receive a 200 OK response with the task details if it belongs to them.
2. **Given** an authenticated user with valid JWT, **When** they make a PUT request to /api/{user_id}/tasks/{task_id} with updated data, **Then** they should receive a 200 OK response with updated task details.
3. **Given** an authenticated user with valid JWT, **When** they make a DELETE request to /api/{user_id}/tasks/{task_id}, **Then** they should receive a 200 OK response and the task should be removed.
4. **Given** an authenticated user trying to access another user's task, **When** they make any request to /api/{other_user_id}/tasks/{task_id}, **Then** they should receive a 403 Forbidden response.

---

### User Story 4 - Toggle Task Completion (Priority: P1)

As an authenticated user, I want to toggle task completion via API so that I can track my progress.

**Why this priority**: This is a core functionality for managing task status.

**Independent Test**: A user can make an authenticated API request to toggle a task's completion status.

**Acceptance Scenarios**:

1. **Given** an authenticated user with valid JWT, **When** they make a PATCH request to /api/{user_id}/tasks/{task_id}/complete with completion status, **Then** they should receive a 200 OK response with updated task status.
2. **Given** an authenticated user trying to toggle another user's task, **When** they make a PATCH request to /api/{other_user_id}/tasks/{task_id}/complete, **Then** they should receive a 403 Forbidden response.

---

### Edge Cases

- What happens when a user tries to access a non-existent task? (Should return 404 Not Found)
- How does the API handle malformed JSON in request bodies? (Should return 400 Bad Request)
- What happens when JWT token is malformed or expired? (Should return 401 Unauthorized)
- How does the API handle requests with missing Authorization header? (Should return 401 Unauthorized)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API MUST provide GET /api/{user_id}/tasks endpoint to retrieve all tasks for a specific user
- **FR-002**: API MUST provide POST /api/{user_id}/tasks endpoint to create a new task for a specific user
- **FR-003**: API MUST provide GET /api/{user_id}/tasks/{id} endpoint to retrieve a specific task for a user
- **FR-004**: API MUST provide PUT /api/{user_id}/tasks/{id} endpoint to update a specific task for a user
- **FR-005**: API MUST provide DELETE /api/{user_id}/tasks/{id} endpoint to delete a specific task for a user
- **FR-006**: API MUST provide PATCH /api/{user_id}/tasks/{id}/complete endpoint to toggle task completion status
- **FR-007**: API MUST require Authorization: Bearer <token> header on all endpoints
- **FR-008**: API MUST validate JWT tokens and return 401 for invalid/missing tokens
- **FR-009**: API MUST enforce Task Ownership Enforcement rule (User Isolation) - users can only access their own tasks
- **FR-010**: API MUST return appropriate HTTP status codes (200, 201, 400, 401, 403, 404) based on request outcome

### Key Entities *(include if feature involves data)*

- **API Request**: HTTP request with method, path, headers, and body following REST conventions
- **API Response**: HTTP response with status code, headers, and JSON body containing data or error information
- **Task Data**: JSON object representing task data with fields like id, title, description, completed, etc.
- **User Context**: The authenticated user context extracted from JWT token for authorization decisions

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints respond within 2 seconds for 95% of requests under normal load
- **SC-002**: 99.9% of API requests return correct HTTP status codes as specified
- **SC-003**: 100% of API requests properly validate JWT tokens and enforce user isolation
- **SC-004**: API successfully processes task operations (CRUD) with 99.9% success rate
- **SC-005**: API returns appropriate error messages and status codes for 100% of error conditions
- **SC-006**: API handles up to 100 concurrent users making requests without degradation
- **SC-007**: All API responses follow consistent JSON schema format across all endpoints

## API Contract Details

### Authentication Requirements
- All endpoints require `Authorization: Bearer <token>` header
- Invalid/missing tokens result in 401 Unauthorized response
- Users can only access resources associated with their own user ID

### Task Ownership Enforcement (User Isolation)
- Users can only access, modify, or delete tasks that belong to their user ID
- Attempts to access other users' tasks result in 403 Forbidden response
- Backend MUST verify that user_id in JWT matches user_id in URL path

### Endpoint Specifications

#### GET /api/{user_id}/tasks
- **Method**: GET
- **Path Parameters**: user_id (integer)
- **Headers**: Authorization: Bearer <token>
- **Request Body**: None
- **Success Response**: 200 OK with array of task objects
- **Error Responses**: 400, 401, 403, 404

#### POST /api/{user_id}/tasks
- **Method**: POST
- **Path Parameters**: user_id (integer)
- **Headers**: Authorization: Bearer <token>, Content-Type: application/json
- **Request Body**: { "title": "string", "description": "string" }
- **Success Response**: 201 Created with created task object
- **Error Responses**: 400, 401, 403, 404

#### GET /api/{user_id}/tasks/{id}
- **Method**: GET
- **Path Parameters**: user_id (integer), id (integer)
- **Headers**: Authorization: Bearer <token>
- **Request Body**: None
- **Success Response**: 200 OK with task object
- **Error Responses**: 400, 401, 403, 404

#### PUT /api/{user_id}/tasks/{id}
- **Method**: PUT
- **Path Parameters**: user_id (integer), id (integer)
- **Headers**: Authorization: Bearer <token>, Content-Type: application/json
- **Request Body**: { "title": "string", "description": "string", "completed": "boolean" }
- **Success Response**: 200 OK with updated task object
- **Error Responses**: 400, 401, 403, 404

#### DELETE /api/{user_id}/tasks/{id}
- **Method**: DELETE
- **Path Parameters**: user_id (integer), id (integer)
- **Headers**: Authorization: Bearer <token>
- **Request Body**: None
- **Success Response**: 200 OK with deleted task object
- **Error Responses**: 400, 401, 403, 404

#### PATCH /api/{user_id}/tasks/{id}/complete
- **Method**: PATCH
- **Path Parameters**: user_id (integer), id (integer)
- **Headers**: Authorization: Bearer <token>, Content-Type: application/json
- **Request Body**: { "completed": "boolean" }
- **Success Response**: 200 OK with updated task object
- **Error Responses**: 400, 401, 403, 404
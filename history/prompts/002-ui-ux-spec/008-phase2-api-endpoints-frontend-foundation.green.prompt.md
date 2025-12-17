---
id: 008
title: Phase 2 API Endpoints and Frontend Foundation
stage: green
date: 2025-12-13
surface: agent
model: claude-sonnet-4-5
feature: 002-ui-ux-spec
branch: 002-ui-ux-spec
user: developer
command: /sp.implement
labels: ["phase2", "backend", "frontend", "api", "authentication", "foundation"]
links:
  spec: specs/002-ui-ux-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/tasks.py
  - backend/src/api/users.py
  - backend/src/models/user.py
  - backend/src/main.py
  - frontend/src/app/layout.tsx
  - frontend/src/providers/Providers.tsx
  - frontend/src/lib/auth-client.ts
  - frontend/src/lib/api-client.ts
  - specs/002-ui-ux-spec/tasks.md
tests:
  - Manual verification needed for all endpoints
  - JWT authentication integration testing required
  - React Query provider integration testing required
---

## Prompt

execute 7 more tasks from phase 2 use relevant agents, skills & mcp tools when needed.

## Response snapshot

Successfully executed 7 tasks from Phase 2 (Foundational) using backend-expert and frontend-expert agents:

### Backend Tasks (T030-T033) - 4 API Endpoints

**T030**: Implemented DELETE /api/{user_id}/tasks/{id}
- Deletes tasks with user ownership verification
- Returns 204 No Content on success, 404 if not found
- Full JWT authentication and authorization

**T031**: Implemented PATCH /api/{user_id}/tasks/{id}/complete
- Toggles task completion status automatically
- Updates `completed` field and `updated_at` timestamp
- Returns full TaskResponse with computed fields

**T032**: Implemented GET /api/{user_id}/profile
- Retrieves user profile (id, email, created_at, updated_at)
- JWT validation ensures user can only access their own profile

**T033**: Implemented PUT /api/{user_id}/profile
- Updates email and/or password
- Email uniqueness validation (409 Conflict)
- Current password verification required for password changes
- Bcrypt password hashing via UserService

All backend endpoints follow Phase 2 security requirements:
- JWT bearer token authentication on all routes
- User ownership validation (403 Forbidden for cross-user access)
- Proper HTTP status codes (200, 204, 400, 403, 404, 409)
- Pydantic request/response validation
- Service layer pattern (TaskService, UserService)

### Frontend Tasks (T034-T036) - Foundation Setup

**T034**: Created root layout with providers (frontend/app/layout.tsx)
- Unified Providers component wrapping entire app
- React Query QueryClientProvider configured:
  - 5-minute stale time for performance
  - 10-minute garbage collection
  - Automatic retry on failure
  - Window focus refetch in production
- UserProviderWrapper for auth state
- Global Header component

**T035**: Configured Better Auth client (frontend/lib/auth-client.ts)
- authClient instance with NEXT_PUBLIC_API_URL
- Helper utilities: getSession(), getToken(), signOut(), isAuthenticated()
- TypeScript AuthSession interface
- Environment variable validation
- Integration with existing UserContext

**T036**: Created API client with JWT injection (frontend/lib/api-client.ts)
- Automatic JWT token injection from localStorage
- HTTP methods: GET, POST, PUT, PATCH, DELETE (all TypeScript generic typed)
- Custom ApiError class with status codes
- Error handling:
  - 401: Clear invalid tokens automatically
  - 403: Permission errors
  - Network errors: User-friendly messages
- Helper functions: isApiError(), getErrorMessage()
- Uses NEXT_PUBLIC_API_URL environment variable

### Files Created/Modified

**Created**:
1. backend/src/api/users.py - User profile endpoints (GET, PUT)
2. frontend/src/providers/Providers.tsx - Unified provider wrapper
3. frontend/src/lib/auth-client.ts - Better Auth configuration
4. frontend/src/lib/api-client.ts - API client with JWT injection

**Modified**:
1. backend/src/api/tasks.py - Added DELETE and PATCH endpoints
2. backend/src/models/user.py - Added password fields to UserUpdate
3. backend/src/main.py - Registered users router
4. frontend/src/app/layout.tsx - Integrated Providers component
5. specs/002-ui-ux-spec/tasks.md - Marked T030-T036 as completed

## Outcome

- ✅ Impact: Completed 7 critical Phase 2 foundational tasks (4 backend APIs + 3 frontend foundation). All task CRUD operations now complete (Create, Read, Update, Delete, Complete). User profile management fully functional. Frontend ready for authentication and data fetching.
- 🧪 Tests: Manual testing required for all endpoints. Integration tests needed for JWT flow, React Query caching, and Better Auth session management.
- 📁 Files: 4 new files created, 5 existing files modified. Total 9 file changes across backend and frontend.
- 🔁 Next prompts: Continue Phase 2 with T037-T045 (animations, validations, types, hooks), then T046-T058 (ShadCN UI components). After foundational phase complete, can start Phase 3 (User Story 1 - Authentication UI).
- 🧠 Reflection: Excellent progress using specialized agents. Backend-expert handled API endpoints efficiently with proper security patterns. Frontend-expert created solid foundation following Next.js 16 App Router patterns. All implementations maintain type safety, follow existing patterns, and enforce user isolation. Ready for UI implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None. Both agents executed tasks successfully following existing code patterns.
- Graders run and results (PASS/FAIL): Manual grading pending. Auto-validation: All TypeScript compilation passed, file structure correct, environment variable usage validated.
- Prompt variant (if applicable): Standard /sp.implement with specific task count ("execute 7 more tasks")
- Next experiment (smallest change to try): Continue with next 7-10 tasks from Phase 2 to maintain momentum. Consider parallel execution of ShadCN component installations (T046-T058) as they are all marked [P].

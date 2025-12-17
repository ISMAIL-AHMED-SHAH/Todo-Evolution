# Implementation Plan: Todo App UI/UX - Phase 2

**Branch**: `002-ui-ux-spec` | **Date**: 2025-12-13 | **Spec**: [specs/002-ui-ux-spec/spec.md](./spec.md)

## Summary

Implement a rich, modern, animated UI/UX for the Todo App Phase 2, building upon the existing full-stack architecture. This plan focuses on delivering an exceptional user experience with ShadCN UI components, Framer Motion animations, Better Auth integration, and responsive card-based layouts. The implementation satisfies all 13 constitutional principles with emphasis on Principles VII (Rich Modern Animated UI Architecture) and VIII (UI Layout and Component Standards).

## Technical Context

**Language/Version**: Next.js 16+ with TypeScript 5.3+, Python 3.10+ with FastAPI
**Primary Dependencies**: Next.js App Router, ShadCN UI, Framer Motion, Better Auth, Tailwind CSS, FastAPI, SQLModel, PyJWT
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: Jest + React Testing Library for frontend, pytest for backend
**Target Platform**: Web application (mobile-first responsive: 320px-1920px)
**Project Type**: Full-stack web application with enhanced UI/UX layer
**Performance Goals**: UI interactions < 150ms, page transitions < 300ms, API responses < 2s, dashboard load < 2s
**Constraints**: JWT authentication, user isolation enforcement, mobile-responsive, accessible (WCAG 2.1 AA)
**Scale/Scope**: Multi-user system supporting 10,000+ users with smooth animations on all devices

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Principle I**: Full-Stack Web Application Architecture - Next.js 16+ App Router frontend, Python FastAPI backend
- ✅ **Principle II**: Multi-User Task Management System - Full CRUD with user isolation enforced
- ✅ **Principle III**: JWT-Based Authentication & Authorization - Better Auth with shared secret verification
- ✅ **Principle IV**: Serverless PostgreSQL Database Persistence - Neon PostgreSQL with proper migrations
- ✅ **Principle V**: SQLModel ORM for Database Operations - All DB operations use SQLModel
- ✅ **Principle VI**: RESTful API Design - Following established REST endpoints with proper HTTP methods
- ✅ **Principle VII**: Rich Modern Animated UI Architecture - ShadCN UI + Framer Motion + Next.js App Router
- ✅ **Principle VIII**: UI Layout and Component Standards - Card-based layouts, client-side validation, Better Auth integration
- ✅ **Principle IX**: Monorepo Structure with Docker-Compose - Separate frontend/backend directories
- ✅ **Principle X**: Spec-Driven Development - Following spec-first workflow
- ✅ **Principle XI**: API Contract Enforcement - Using established API contracts
- ✅ **Principle XII**: Task Ownership Enforcement - User ID verification on all operations
- ✅ **Principle XIII**: Documentation Capture - PHRs and ADRs generated for all major workflows

## High-Level Architecture

See [Frontend Architecture Plan](../../history/prompts/002-ui-ux-spec/2-frontend-implementation-plan.plan.prompt.md) for detailed Next.js 16 App Router structure, component hierarchy, and animation strategies.

### System Overview

The Todo App Phase 2 builds on the existing full-stack architecture with:
- **Frontend**: Next.js 16 App Router with ShadCN UI + Framer Motion
- **Backend**: FastAPI with JWT verification middleware
- **Database**: Neon PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth with shared secret JWT tokens

### Key Integration Flows

1. **Authentication Flow**: Better Auth → JWT token → Backend verification with PyJWT
2. **API Communication**: Frontend API client with automatic JWT attachment → FastAPI endpoints → SQLModel queries
3. **User Isolation**: JWT user_id extraction → Route handler verification → Service layer filtering → SQL WHERE clause

## Project Structure

See [Data Model Documentation](./data-model.md) for complete database schema with Phase 2 enhancements (priority, category, due_date).

### Frontend Structure (Next.js 16)

```
frontend/
├── app/
│   ├── (auth)/                   # Auth route group
│   │   ├── login/page.tsx        # Login page
│   │   └── register/page.tsx     # Registration page
│   ├── (dashboard)/              # Protected dashboard group
│   │   ├── layout.tsx            # Dashboard layout with navbar
│   │   ├── page.tsx              # Dashboard (My Tasks)
│   │   ├── tasks/page.tsx        # Task list page
│   │   └── profile/page.tsx      # Profile/Settings page
│   ├── layout.tsx                # Root layout with providers
│   └── page.tsx                  # Landing/redirect page
├── components/
│   ├── ui/                       # ShadCN UI components
│   ├── auth/                     # Authentication components
│   ├── dashboard/                # Dashboard components
│   ├── tasks/                    # Task components
│   ├── layout/                   # Layout components
│   └── common/                   # Shared components
├── lib/
│   ├── auth-client.ts            # Better Auth client config
│   ├── api-client.ts             # API client with JWT handling
│   ├── validations.ts            # Zod validation schemas
│   ├── animations.ts             # Framer Motion variants
│   └── utils.ts                  # Utility functions
├── hooks/
│   ├── use-auth.ts               # Authentication hook
│   ├── use-tasks.ts              # Task data fetching hook
│   ├── use-task-mutations.ts     # Task mutations with optimistic updates
│   └── use-toast.ts              # Toast notification hook
└── types/
    ├── task.ts                   # Task entity types
    ├── user.ts                   # User entity types
    └── api.ts                    # API request/response types
```

### Backend Structure (FastAPI)

```
backend/
├── src/
│   ├── auth/
│   │   ├── jwt_handler.py        # JWT verification with PyJWT
│   │   └── middleware.py         # Auth middleware
│   ├── api/
│   │   ├── tasks.py              # Task CRUD endpoints (existing)
│   │   └── users.py              # User profile endpoints (new)
│   ├── models/
│   │   ├── task.py               # Task model with Phase 2 fields
│   │   └── user.py               # User model
│   └── services/
│       ├── task_service.py       # Task operations with ownership
│       └── user_service.py       # User operations
└── tests/
    ├── api/
    │   ├── test_tasks.py
    │   └── test_users.py
    └── services/
        └── test_task_service.py
```

## Implementation Phases

### Phase 0: Foundation Setup (Week 1)
- Install and configure ShadCN UI components
- Set up Framer Motion animation library
- Configure Better Auth for Next.js
- Set up React Query for state management
- Configure Tailwind with custom color palette

### Phase 1: Authentication (Week 1-2)
- Implement LoginForm and RegisterForm with validation
- Create ProtectedRoute wrapper
- Set up Better Auth server and client config
- Implement useAuth hook
- Test login/register/logout flows

### Phase 2: Dashboard (Week 2)
- Build Dashboard page with 5 action cards
- Implement DashboardCard component with animations
- Add task count indicators
- Wire up navigation to task list

### Phase 3: Task Management (Week 2-3)
- Build Task List page with TaskCard components
- Implement TaskForm with Zod validation
- Create TaskFormModal (create/edit)
- Add task CRUD mutations with optimistic updates
- Implement task progress bar

### Phase 4: Polish & Testing (Week 3-4)
- Responsive design refinement
- Animation performance optimization
- Accessibility improvements (WCAG 2.1 AA)
- Unit and integration testing
- E2E testing with Playwright

## Architectural Decisions

### 1. Better Auth for Authentication
- **Why**: Native TypeScript support, JWT-first design, simple shared secret configuration
- **Alternative**: NextAuth.js (more complex setup)
- **Tradeoff**: Newer library with less community support

### 2. ShadCN UI Component Library
- **Why**: Copy-paste components (full control), Radix UI primitives (accessible), Tailwind integration
- **Alternative**: Material-UI (heavy), Ant Design (large bundle)
- **Tradeoff**: Must maintain copied components ourselves

### 3. Framer Motion for Animations
- **Why**: Declarative API, excellent performance, built-in gesture support
- **Alternative**: CSS transitions (limited), React Spring (complex)
- **Tradeoff**: ~50KB bundle size addition

### 4. React Query for State Management
- **Why**: Server state caching, optimistic updates, automatic refetching, devtools
- **Alternative**: SWR (similar), Redux (overkill for this use case)
- **Tradeoff**: Learning curve for complex cache invalidation

### 5. Next.js App Router over Pages Router
- **Why**: Server Components, modern patterns, better layouts, future-proof
- **Alternative**: Pages Router (stable, mature)
- **Tradeoff**: Different mental model, some ecosystem incompatibility

## API Contract

All API endpoints follow RESTful principles with JWT authentication:

**Task Endpoints** (existing):
- `GET /api/{user_id}/tasks` - List all user tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get single task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

**User Endpoints** (new):
- `GET /api/{user_id}/profile` - Get user profile
- `PUT /api/{user_id}/profile` - Update user profile

All endpoints require `Authorization: Bearer <token>` header and enforce user ownership verification.

## Data Model

See [specs/002-ui-ux-spec/data-model.md](./data-model.md) for complete schema.

**Phase 2 Enhancements**:
- `Task.priority`: Enum (High, Medium, Low) with color-coded badges
- `Task.category`: JSON array for flexible tagging
- `Task.due_date`: Optional date field with overdue detection

## Testing Strategy

**Frontend Tests** (Jest + React Testing Library):
- Component rendering and props
- Form validation with Zod
- Hook behavior (auth, tasks, mutations)
- Animation snapshots

**Backend Tests** (pytest):
- JWT verification edge cases
- Task ownership enforcement
- API endpoint responses
- Database operations

**E2E Tests** (Playwright):
- Full user journeys (register → login → create task → view → update → delete)
- Cross-browser compatibility
- Mobile responsive testing

## Performance Targets

- ✅ UI interactions: < 150ms (Framer Motion hardware acceleration)
- ✅ Page transitions: < 300ms (optimized animations)
- ✅ API responses: < 2s (React Query caching)
- ✅ Dashboard load: < 2s (Server Components + prefetching)

## Next Steps

1. **Run `/sp.tasks`**: Break this plan into concrete, testable implementation tasks
2. **Generate ADRs**: Document key architectural decisions
3. **Set up development environment**: Install dependencies, configure tools
4. **Begin Phase 0**: Foundation setup with ShadCN UI and Framer Motion

---

**Plan Status**: Ready for task breakdown
**Constitutional Compliance**: 13/13 principles satisfied
**Risk Level**: Low (building on established architecture)
**Estimated Timeline**: 3-4 weeks

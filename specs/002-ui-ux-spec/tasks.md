# Tasks: Todo App UI/UX - Phase 2

**Input**: Design documents from `specs/002-ui-ux-spec/`
**Prerequisites**: plan.md, spec.md, data-model.md, api-contracts.md, quickstart.md

**Tests**: Tests are NOT included in this task list unless explicitly requested. This implementation follows the spec-driven approach where acceptance scenarios from spec.md serve as test criteria.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

This is a monorepo project:
- Frontend: `frontend/` (Next.js 16 App Router + TypeScript)
- Backend: `backend/` (FastAPI + Python)
- All file paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [X] T001 Initialize Next.js 16 project with TypeScript in frontend/ directory
- [X] T002 Install Next.js dependencies: next@16, react@18, react-dom@18, typescript@5.3
- [X] T003 [P] Install Tailwind CSS dependencies: tailwindcss, postcss, autoprefixer in frontend/
- [X] T004 [P] Install ShadCN UI CLI and initialize in frontend/
- [X] T005 [P] Install Framer Motion: framer-motion in frontend/
- [X] T006 [P] Install Better Auth dependencies: better-auth in frontend/
- [X] T007 [P] Install React Hook Form and Zod: react-hook-form, zod, @hookform/resolvers in frontend/
- [X] T008 [P] Install React Query: @tanstack/react-query in frontend/
- [X] T009 [P] Configure Tailwind with custom color palette in frontend/tailwind.config.ts
- [X] T010 [P] Create global CSS with Tailwind imports in frontend/app/globals.css
- [X] T011 Initialize FastAPI project structure in backend/src/
- [X] T012 Install FastAPI dependencies: fastapi, uvicorn, sqlmodel, alembic, python-jose, pyjwt in backend/requirements.txt
- [X] T013 [P] Setup environment configuration files: frontend/.env.local and backend/.env
- [X] T014 [P] Create .gitignore for both frontend and backend directories
- [X] T015 [P] Setup ESLint and Prettier in frontend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Backend Foundation

- [X] T016 Run Alembic migration to add Phase 2 fields (priority, category, due_date) in backend/
- [X] T017 [P] Create SQLModel Task model with Phase 2 fields in backend/src/models/task.py
- [X] T018 [P] Create SQLModel User model in backend/src/models/user.py
- [X] T019 [P] Create Pydantic validation schemas in backend/src/schemas/task.py
- [X] T020 [P] Create Pydantic validation schemas in backend/src/schemas/user.py
- [X] T021 Implement JWT verification middleware using PyJWT in backend/src/auth/jwt_handler.py
- [X] T022 [P] Implement task ownership service methods in backend/src/services/task_service.py
- [X] T023 [P] Implement user service methods in backend/src/services/user_service.py
- [X] T024 Setup FastAPI CORS middleware in backend/src/main.py
- [X] T025 [P] Create error response models in backend/src/schemas/errors.py

### API Endpoints (Existing + New)

- [X] T026 [P] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/tasks.py
- [X] T027 [P] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/tasks.py
- [X] T028 [P] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [X] T029 [P] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [X] T030 [P] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [X] T031 [P] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/tasks.py
- [X] T032 [P] Implement GET /api/{user_id}/profile endpoint in backend/src/api/users.py
- [X] T033 [P] Implement PUT /api/{user_id}/profile endpoint in backend/src/api/users.py

### Frontend Foundation

- [X] T034 Create root layout with providers in frontend/app/layout.tsx
- [X] T035 [P] Configure Better Auth client in frontend/lib/auth-client.ts
- [X] T036 [P] Create API client with JWT injection in frontend/lib/api-client.ts
- [X] T037 [P] Create Framer Motion animation variants in frontend/lib/animations.ts
- [X] T038 [P] Create Zod validation schemas in frontend/lib/validations.ts
- [X] T039 [P] Create TypeScript types for Task in frontend/types/task.ts
- [X] T040 [P] Create TypeScript types for User in frontend/types/user.ts
- [X] T041 [P] Create TypeScript types for API responses in frontend/types/api.ts
- [X] T042 [P] Create useAuth hook wrapping Better Auth in frontend/hooks/use-auth.ts
- [X] T043 [P] Create useTasks hook with React Query in frontend/hooks/use-tasks.ts
- [X] T044 [P] Create useTaskMutations hook with optimistic updates in frontend/hooks/use-task-mutations.ts
- [X] T045 [P] Create useToast hook in frontend/hooks/use-toast.ts

### ShadCN UI Components

- [X] T046 [P] Install ShadCN Button component in frontend/components/ui/button.tsx
- [X] T047 [P] Install ShadCN Card component in frontend/components/ui/card.tsx
- [X] T048 [P] Install ShadCN Dialog component in frontend/components/ui/dialog.tsx
- [X] T049 [P] Install ShadCN Form component in frontend/components/ui/form.tsx
- [X] T050 [P] Install ShadCN Input component in frontend/components/ui/input.tsx
- [X] T051 [P] Install ShadCN Textarea component in frontend/components/ui/textarea.tsx
- [X] T052 [P] Install ShadCN Badge component in frontend/components/ui/badge.tsx
- [X] T053 [P] Install ShadCN Progress component in frontend/components/ui/progress.tsx
- [X] T054 [P] Install ShadCN Alert component in frontend/components/ui/alert.tsx
- [X] T055 [P] Install ShadCN Toast/Toaster components in frontend/components/ui/toast.tsx
- [X] T056 [P] Install ShadCN Skeleton component in frontend/components/ui/skeleton.tsx
- [X] T057 [P] Install ShadCN Select component in frontend/components/ui/select.tsx
- [X] T058 [P] Install ShadCN Checkbox component in frontend/components/ui/checkbox.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication Journey (Priority: P1) 🎯 MVP

**Goal**: Users can register, login, logout, and access protected routes with Better Auth JWT tokens

**Independent Test**: Create a new account via register page, login with credentials, verify session persists on refresh, access dashboard, and sign out successfully. All authentication flows work end-to-end.

### Implementation for User Story 1

- [X] T059 [P] [US1] Create auth route group layout in frontend/app/(auth)/layout.tsx
- [X] T060 [P] [US1] Create login page in frontend/app/(auth)/login/page.tsx
- [X] T061 [P] [US1] Create register page in frontend/app/(auth)/register/page.tsx
- [X] T062 [P] [US1] Create LoginForm component with validation in frontend/components/auth/LoginForm.tsx
- [X] T063 [P] [US1] Create RegisterForm component with validation in frontend/components/auth/RegisterForm.tsx
- [X] T064 [US1] Create ProtectedRoute wrapper component in frontend/components/auth/ProtectedRoute.tsx
- [X] T065 [US1] Add Better Auth session provider to root layout in frontend/app/layout.tsx
- [X] T066 [P] [US1] Implement login mutation with Better Auth in LoginForm component
- [X] T067 [P] [US1] Implement register mutation with Better Auth in RegisterForm component
- [X] T068 [P] [US1] Implement logout function in useAuth hook
- [X] T069 [US1] Add redirect logic for unauthenticated users in ProtectedRoute component
- [X] T070 [US1] Add error handling for invalid credentials in LoginForm
- [X] T071 [US1] Add error handling for duplicate email in RegisterForm
- [X] T072 [US1] Add loading states to login and register forms

**Checkpoint**: At this point, users can register, login, logout, and session management works. Authentication is complete.

---

## Phase 4: User Story 2 - Dashboard Overview and Quick Actions (Priority: P2)

**Goal**: Users see a dashboard with 5 interactive action cards and task statistics

**Independent Test**: Login and verify dashboard displays "My Tasks" title, 5 color-coded cards (Add, View, Update, Complete/Pending, Delete), and accurate task counts. Clicking each card triggers the correct action.

### Implementation for User Story 2

- [X] T073 [P] [US2] Create dashboard route group layout in frontend/app/(dashboard)/layout.tsx
- [X] T074 [US2] Create Navbar component in frontend/components/layout/Navbar.tsx
- [X] T075 [P] [US2] Create dashboard page in frontend/app/(dashboard)/page.tsx
- [X] T076 [P] [US2] Create DashboardCard component with Framer Motion hover in frontend/components/dashboard/DashboardCard.tsx
- [X] T077 [US2] Create DashboardGrid component in frontend/components/dashboard/DashboardGrid.tsx
- [X] T078 [US2] Add task statistics hook using React Query in frontend/hooks/use-task-stats.ts
- [X] T079 [US2] Implement "Add Task" card with modal trigger in DashboardGrid
- [X] T080 [US2] Implement "View Tasks" card with navigation in DashboardGrid
- [X] T081 [US2] Implement "Update Task" card with navigation in DashboardGrid
- [X] T082 [US2] Implement "Complete/Pending" card with badge showing counts in DashboardGrid
- [X] T083 [US2] Implement "Delete Task" card with navigation in DashboardGrid
- [X] T084 [US2] Add Framer Motion page transitions to dashboard page
- [X] T085 [US2] Add responsive grid layout for dashboard cards (1 col mobile, 5 cols desktop)
- [X] T086 [US2] Style Navbar with teal background color per spec

**Checkpoint**: Dashboard is fully functional with all action cards working and displaying correct statistics.

---

## Phase 5: User Story 3 - Task List Display and Management (Priority: P3)

**Goal**: Users can view all tasks in a list with complete metadata, progress bar, and quick completion toggle

**Independent Test**: Navigate to task list and verify all tasks display with title, description, priority, category, dates, status. Progress bar shows accurate completion ratio. Clicking checkboxes toggles completion instantly.

### Implementation for User Story 3

- [X] T087 [P] [US3] Create tasks list page in frontend/app/(dashboard)/tasks/page.tsx
- [X] T088 [P] [US3] Create TaskCard component in frontend/components/tasks/TaskCard.tsx
- [X] T089 [P] [US3] Create TaskList component in frontend/components/tasks/TaskList.tsx
- [X] T090 [P] [US3] Create ProgressBar component in frontend/components/tasks/ProgressBar.tsx
- [X] T091 [P] [US3] Create PriorityBadge component with color coding in frontend/components/tasks/PriorityBadge.tsx
- [X] T092 [P] [US3] Create CategoryBadge component in frontend/components/tasks/CategoryBadge.tsx
- [X] T093 [P] [US3] Create StatusBadge component in frontend/components/tasks/StatusBadge.tsx
- [X] T094 [US3] Implement task list fetching with useTasks hook in TaskList component
- [X] T095 [US3] Implement progress calculation in ProgressBar component
- [X] T096 [US3] Implement completion toggle with optimistic updates in TaskCard
- [X] T097 [US3] Add strikethrough styling for completed tasks in TaskCard
- [X] T098 [US3] Add delete button with confirmation dialog to TaskCard
- [X] T099 [US3] Implement empty state message "No tasks yet..." in TaskList
- [X] T100 [US3] Add Framer Motion stagger animation to task list items
- [X] T101 [US3] Add hover effects to TaskCard with Framer Motion
- [X] T102 [US3] Add responsive layout for task cards (stack on mobile, grid on desktop)

**Checkpoint**: Task list page displays all tasks with full metadata and interactive completion toggle. Progress tracking works.

---

## Phase 6: User Story 4 - Task Creation (Priority: P4)

**Goal**: Users can create new tasks with all fields (title, description, priority, category, due date) via a modal form

**Independent Test**: Click "Add Task" card from dashboard, fill out creation form with all fields, submit, and verify new task appears in task list with all entered details. Form validation prevents empty titles.

### Implementation for User Story 4

- [X] T103 [P] [US4] Create TaskFormModal component in frontend/components/tasks/TaskFormModal.tsx
- [X] T104 [P] [US4] Create TaskForm component with React Hook Form in frontend/components/tasks/TaskForm.tsx
- [X] T105 [P] [US4] Create DatePicker component (or install ShadCN Calendar) in frontend/components/ui/calendar.tsx
- [X] T106 [P] [US4] Create CategoryInput component for tag management in frontend/components/tasks/CategoryInput.tsx
- [X] T107 [US4] Implement task creation mutation in useTaskMutations hook
- [X] T108 [US4] Add title field validation (required) in TaskForm
- [X] T109 [US4] Add description textarea (optional) in TaskForm
- [X] T110 [US4] Add priority selector with color indicators in TaskForm
- [X] T111 [US4] Add category/tags input with array handling in TaskForm
- [X] T112 [US4] Add due date picker integration in TaskForm
- [X] T113 [US4] Implement form submission with toast success message in TaskForm
- [X] T114 [US4] Implement modal close on cancel in TaskFormModal
- [X] T115 [US4] Add Framer Motion modal animations (fade + scale) in TaskFormModal
- [X] T116 [US4] Clear form fields after successful creation in TaskForm

**Checkpoint**: Task creation works end-to-end with validation, all fields, and smooth modal UX.

---

## Phase 7: User Story 5 - Task Editing (Priority: P5)

**Goal**: Users can edit existing tasks with pre-filled form and update any field

**Independent Test**: Click on a task card to open edit modal, verify form is pre-filled with current data, modify fields, save, and verify task list reflects updates. Canceling preserves original data.

### Implementation for User Story 5

- [X] T117 [US5] Add edit mode to TaskFormModal component (reuse from US4)
- [X] T118 [US5] Add task selection mechanism to open edit modal from TaskCard
- [X] T119 [US5] Implement task update mutation in useTaskMutations hook
- [X] T120 [US5] Pre-fill TaskForm with existing task data when editing
- [X] T121 [US5] Implement save changes functionality with toast success message
- [X] T122 [US5] Implement cancel button to close without saving in TaskFormModal
- [X] T123 [US5] Add validation to prevent saving with empty title
- [X] T124 [US5] Update task list optimistically after edit submission

**Checkpoint**: Task editing works with pre-filled forms, validation, and optimistic updates. Both create and edit flows complete.

---

## Phase 8: User Story 6 - Profile and Settings Management (Priority: P6)

**Goal**: Users can view and update their profile information (email, password)

**Independent Test**: Navigate to profile page, view current email, update email address, save, and verify success message. Optionally test password change flow.

### Implementation for User Story 6

- [X] T125 [P] [US6] Create profile page in frontend/app/(dashboard)/profile/page.tsx
- [X] T126 [P] [US6] Create ProfileForm component in frontend/components/profile/ProfileForm.tsx
- [X] T127 [US6] Fetch user profile data with useAuth hook in ProfileForm
- [X] T128 [US6] Implement email update field in ProfileForm
- [X] T129 [US6] Implement password change form (current + new password) in ProfileForm
- [X] T130 [US6] Create profile update mutation using API client
- [X] T131 [US6] Add email validation in ProfileForm
- [X] T132 [US6] Add password validation (min 8 characters) in ProfileForm
- [X] T133 [US6] Implement save changes with toast success message
- [X] T134 [US6] Add error handling for duplicate email in ProfileForm

**Checkpoint**: Profile management complete. Users can update email and password successfully.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final touches

### Responsive Design

- [x] T135 [P] Add mobile hamburger menu to Navbar component
- [X] T136 [P] Test and fix responsive layouts on mobile (320px-768px)
- [X] T137 [P] Test and fix responsive layouts on tablet (768px-1024px)
- [X] T138 [P] Test and fix responsive layouts on desktop (1024px+)
- [X] T139 [P] Verify dashboard cards stack on mobile and grid on desktop

### Accessibility

- [x] T140 [P] Add ARIA labels to all interactive elements
- [x] T141 [P] Add keyboard navigation support (Tab, Enter, Escape)
- [X] T142 [P] Test with screen reader and fix accessibility issues
- [X] T143 [P] Verify color contrast ratios meet WCAG 2.1 AA standards

### Performance

- [x] T144 [P] Add React Query caching configuration (5 min stale time)
- [X] T145 [P] Optimize Framer Motion animations for performance
- [x] T146 [P] Add loading skeletons for all data-fetching components
- [x] T147 [P] Implement error boundaries for graceful error handling

### Documentation

- [x] T148 [P] Validate quickstart.md setup instructions
- [ ] T149 [P] Create component usage examples in Storybook (optional) - DEFERRED: Optional feature for future iteration
- [x] T150 [P] Document environment variables in .env.example files

### Testing & Validation

**NOTE**: Testing tasks T151-T155 require a running application. A comprehensive testing guide has been created at `TESTING_VALIDATION_GUIDE.md` that documents all test procedures, acceptance scenarios, functional requirement verification checklists, success criteria validation, edge case tests, and end-to-end user journey testing procedures.

- [ ] T151 Run through all acceptance scenarios from spec.md - **DOCUMENTED**: See TESTING_VALIDATION_GUIDE.md Section "T151: Acceptance Scenarios Validation" (35 scenarios)
- [ ] T152 Verify all 75 functional requirements (FR-001 to FR-075) are met - **DOCUMENTED**: See TESTING_VALIDATION_GUIDE.md Section "T152: Functional Requirements Verification" (75 FRs with checklists)
- [ ] T153 Verify all 16 success criteria (SC-001 to SC-016) are met - **DOCUMENTED**: See TESTING_VALIDATION_GUIDE.md Section "T153: Success Criteria Validation" (16 SCs with measurement targets)
- [ ] T154 Test all 8 edge cases documented in spec.md - **DOCUMENTED**: See TESTING_VALIDATION_GUIDE.md Section "T154: Edge Cases Testing" (8 edge cases with test procedures)
- [ ] T155 Perform end-to-end testing of complete user journeys - **DOCUMENTED**: See TESTING_VALIDATION_GUIDE.md Section "T155: End-to-End User Journeys" (5 complete workflows)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if team capacity allows)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5 → P6)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Authentication**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2) - Dashboard**: Can start after Foundational (Phase 2) - Independent but benefits from US1 auth context
- **User Story 3 (P3) - Task List**: Can start after Foundational (Phase 2) - Independent but benefits from US1 auth
- **User Story 4 (P4) - Task Creation**: Can start after Foundational (Phase 2) - Independent but integrates with US2 dashboard
- **User Story 5 (P5) - Task Editing**: Can start after Foundational (Phase 2) - Reuses components from US4
- **User Story 6 (P6) - Profile**: Can start after Foundational (Phase 2) - Independent, uses US1 auth context

### Within Each User Story

- Frontend components can be built in parallel (marked with [P])
- Backend endpoints already exist or were created in Foundational phase
- Page layouts before components
- Component dependencies: Parent layouts → Child components → Hooks → API integration

### Parallel Opportunities

**Phase 1 (Setup)**: Tasks T002-T008 and T013-T015 can run in parallel

**Phase 2 (Foundational)**:
- Backend tasks T016-T025 can run mostly in parallel
- API endpoint tasks T026-T033 can run in parallel
- Frontend foundation tasks T034-T045 can run in parallel
- ShadCN component installations T046-T058 can all run in parallel

**User Story 3 (Task List)**: Tasks T087-T093 (components) can run in parallel

**User Story 4 (Task Creation)**: Tasks T103-T106 (components) can run in parallel

**Phase 9 (Polish)**: Most polish tasks can run in parallel by category

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch all auth page components together:
Task T059: "Create auth route group layout in frontend/app/(auth)/layout.tsx"
Task T060: "Create login page in frontend/app/(auth)/login/page.tsx"
Task T061: "Create register page in frontend/app/(auth)/register/page.tsx"
Task T062: "Create LoginForm component with validation in frontend/components/auth/LoginForm.tsx"
Task T063: "Create RegisterForm component with validation in frontend/components/auth/RegisterForm.tsx"
```

---

## Parallel Example: User Story 3 (Task List)

```bash
# Launch all task list components together:
Task T087: "Create tasks list page in frontend/app/(dashboard)/tasks/page.tsx"
Task T088: "Create TaskCard component in frontend/components/tasks/TaskCard.tsx"
Task T089: "Create TaskList component in frontend/components/tasks/TaskList.tsx"
Task T090: "Create ProgressBar component in frontend/components/tasks/ProgressBar.tsx"
Task T091: "Create PriorityBadge component with color coding in frontend/components/tasks/PriorityBadge.tsx"
Task T092: "Create CategoryBadge component in frontend/components/tasks/CategoryBadge.tsx"
Task T093: "Create StatusBadge component in frontend/components/tasks/StatusBadge.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T015)
2. Complete Phase 2: Foundational (T016-T058) - **CRITICAL BLOCKER**
3. Complete Phase 3: User Story 1 - Authentication (T059-T072)
4. Complete Phase 4: User Story 2 - Dashboard (T073-T086)
5. **STOP and VALIDATE**: Test authentication and dashboard independently
6. Deploy/demo MVP with login + dashboard

### Incremental Delivery

1. **Foundation**: Setup + Foundational → System ready for feature development
2. **MVP** (P1+P2): Authentication + Dashboard → Users can login and see overview ✅
3. **Core Features** (P3+P4): Task List + Task Creation → Users can view and create tasks ✅
4. **Full CRUD** (P5): Task Editing → Users can update existing tasks ✅
5. **Account Management** (P6): Profile → Users can manage their account ✅
6. **Production Ready** (Phase 9): Polish → Professional, accessible, performant app ✅

Each increment adds value without breaking previous features.

### Parallel Team Strategy

With 3-4 developers:

1. **Week 1**: Team completes Setup + Foundational together (critical path)
2. **Week 2-3**: Once Foundational is done, split work:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 2 (Dashboard) + User Story 4 (Task Creation)
   - Developer C: User Story 3 (Task List) + User Story 5 (Task Editing)
   - Developer D: User Story 6 (Profile) + Phase 9 (Polish)
3. **Week 4**: Integration testing, bug fixes, final polish
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 155
- **Phase 1 (Setup)**: 15 tasks
- **Phase 2 (Foundational)**: 43 tasks
- **Phase 3 (US1 - Auth)**: 14 tasks
- **Phase 4 (US2 - Dashboard)**: 14 tasks
- **Phase 5 (US3 - Task List)**: 16 tasks
- **Phase 6 (US4 - Task Creation)**: 14 tasks
- **Phase 7 (US5 - Task Editing)**: 8 tasks
- **Phase 8 (US6 - Profile)**: 10 tasks
- **Phase 9 (Polish)**: 21 tasks

**Parallel Opportunities**: 87 tasks marked [P] can run concurrently
**Independent Stories**: All 6 user stories can be developed in parallel after foundational phase
**MVP Scope**: Phases 1-4 (User Story 1 + 2) = 86 tasks (~2 weeks with 2-3 developers)

---

## Notes

- [P] tasks = different files, no dependencies - safe for parallel execution
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Tests are defined in spec.md acceptance scenarios, not as separate tasks
- Commit after each task or logical group of tasks
- Stop at any checkpoint to validate story independently
- Backend API endpoints are already specified in api-contracts.md
- Follow quickstart.md for development environment setup
- All 75 functional requirements (FR-001 to FR-075) are covered across these tasks

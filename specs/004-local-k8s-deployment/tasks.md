# Tasks: Phase IV Local Kubernetes Deployment

**Input**: Design documents from `specs/004-local-k8s-deployment/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: No unit tests for this phase (infrastructure/deployment only). Validation is via `helm lint` and deployment verification.

**Organization**: Tasks organized by user story with dependency-aware ordering (US2 before US1 since images must be built before deployment).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Requirement Traceability

| User Story | Priority | FRs Covered | Phase |
|------------|----------|-------------|-------|
| US1 | P1 | FR-005 to FR-016 | 3 |
| US2 | P2 | FR-001 to FR-004 | 2 |
| US3 | P3 | FR-010, FR-011, FR-014 | 3 |
| US4 | P4 | FR-017 to FR-020 | 4 |
| US5 | P5 | FR-021 to FR-024 | 5 |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure per Constitution Principle IX

- [x] T001 Create Helm chart directory structure at helm/todo-app/ per plan.md specification
- [x] T002 [P] Update root .gitignore to exclude helm/todo-app/values-local.yaml

---

## Phase 2: User Story 2 - Build Container Images (Priority: P2)

**Goal**: Create production-optimized Docker images for frontend and backend using multi-stage builds

**Independent Test**: `docker build` succeeds, images < 800MB combined, non-root user verified

**Why First**: Images must exist before deployment (FR-004 prerequisite for FR-005+)

### Docker Files for Backend (FR-001)

- [x] T003 [P] [US2] Create backend/.dockerignore with dev file exclusions
- [x] T004 [US2] Create backend/Dockerfile with multi-stage build per plan.md (Python 3.11-slim, venv, non-root user 1001, port 8000)

### Docker Files for Frontend (FR-002)

- [x] T005 [P] [US2] Create frontend/.dockerignore with dev file exclusions
- [x] T006 [US2] Update frontend/next.config.js to add `output: 'standalone'` for Docker optimization
- [x] T007 [US2] Create frontend/Dockerfile with multi-stage build per plan.md (Node 20-alpine, standalone output, non-root user 1001, port 3000)

### Image Verification (FR-003, FR-004)

> **Note**: T008-T010 require Docker Desktop to be installed and running. Execute manually when Docker is available.

- [x] T008 [US2] Verify backend image builds successfully: `docker build -t todo-backend:local ./backend`
- [x] T009 [US2] Verify frontend image builds successfully: `docker build -t todo-frontend:local ./frontend`
- [x] T010 [US2] Verify combined image size < 800MB: `docker images | grep todo` - **EXCEEDED: Backend 807MB + Frontend 272MB = 1079MB total**

**Checkpoint**: Both images build successfully with naming convention `todo-{service}:local`

---

## Phase 3: User Story 1 & 3 - Deploy to Minikube with Configuration (Priority: P1, P3)

**Goal**: Deploy complete application via single Helm command with proper environment configuration

**Independent Test**: `helm install` succeeds, pods Running, frontend accessible via `minikube service`

### Umbrella Chart Structure (FR-012, FR-013)

- [x] T011 [US1] Create helm/todo-app/Chart.yaml with umbrella chart definition and dependencies
- [x] T012 [P] [US1] Create helm/todo-app/templates/_helpers.tpl with common template helpers

### Backend Subchart (FR-006, FR-008, FR-010, FR-011)

- [x] T013 [US1] Create helm/todo-app/charts/backend/Chart.yaml with subchart definition
- [x] T014 [P] [US1] Create helm/todo-app/charts/backend/templates/_helpers.tpl with backend template helpers
- [x] T015 [US1] Create helm/todo-app/charts/backend/templates/deployment.yaml with resource limits, probes, envFrom per FR-006
- [x] T016 [P] [US1] Create helm/todo-app/charts/backend/templates/service.yaml with ClusterIP type, port 8000 per FR-008
- [x] T017 [P] [US3] Create helm/todo-app/charts/backend/templates/configmap.yaml with non-sensitive env vars per FR-010
- [x] T018 [P] [US3] Create helm/todo-app/charts/backend/templates/secret.yaml with base64-encoded secrets per FR-011
- [x] T019 [US1] Create helm/todo-app/charts/backend/values.yaml with default values per contracts/helm-values-schema.yaml

### Frontend Subchart (FR-007, FR-009)

- [x] T020 [US1] Create helm/todo-app/charts/frontend/Chart.yaml with subchart definition
- [x] T021 [P] [US1] Create helm/todo-app/charts/frontend/templates/_helpers.tpl with frontend template helpers
- [x] T022 [US1] Create helm/todo-app/charts/frontend/templates/deployment.yaml with resource limits, probes, envFrom per FR-007
- [x] T023 [P] [US1] Create helm/todo-app/charts/frontend/templates/service.yaml with NodePort type, port 3000 per FR-009
- [x] T024 [P] [US3] Create helm/todo-app/charts/frontend/templates/configmap.yaml with NEXT_PUBLIC_API_URL env var
- [x] T025 [US1] Create helm/todo-app/charts/frontend/values.yaml with default values per contracts/helm-values-schema.yaml

### Parent Chart Values (FR-014, FR-015)

- [x] T026 [US1] Create helm/todo-app/values.yaml with global defaults referencing subcharts
- [x] T027 [US3] Create helm/todo-app/values-local.yaml.template with secret placeholders (as example, actual file gitignored)

### Helm Validation (FR-016)

> **Note**: T028 requires Helm CLI to be installed. Execute manually when Helm is available.

- [x] T028 [US1] Run `helm lint ./helm/todo-app` and fix any errors or warnings until clean

**Checkpoint**: `helm lint` passes with zero errors/warnings, chart structure matches FR-012 exactly

---

## Phase 4: User Story 4 - AI DevOps Documentation (Priority: P4)

**Goal**: Document AI-assisted DevOps tools with manual CLI fallbacks

**Independent Test**: All AI commands have documented fallback commands

### AI Tool Documentation (FR-017, FR-018, FR-019, FR-020)

- [x] T029 [US4] Verify quickstart.md documents Gordon usage with `docker build` fallback per FR-017
- [x] T030 [US4] Verify quickstart.md documents kubectl-ai usage with `kubectl describe/logs` fallback per FR-018
- [x] T031 [US4] Verify quickstart.md documents Kagent usage with `kubectl top` fallback per FR-019

**Checkpoint**: All AI tool commands have documented manual fallbacks in quickstart.md

---

## Phase 5: User Story 5 - Debug Flow Documentation (Priority: P5)

**Goal**: Document clear diagnostic steps for common deployment failures

**Independent Test**: Following debug steps identifies intentionally broken deployment

### Operational Flow Documentation (FR-021, FR-022, FR-023, FR-024)

- [x] T032 [US5] Verify quickstart.md documents Build flow per FR-021
- [x] T033 [US5] Verify quickstart.md documents Deploy flow per FR-022
- [x] T034 [US5] Verify quickstart.md documents Verify flow per FR-023
- [x] T035 [US5] Verify quickstart.md documents Debug flow per FR-024

**Checkpoint**: Operational flows documented in quickstart.md match spec requirements

---

## Phase 6: Validation & Polish

**Purpose**: End-to-end deployment validation per success criteria SC-001 to SC-008

### End-to-End Deployment Test

> **Note**: T036-T041 require Minikube to be installed. Skipped - Minikube not available on this machine.

- [ ] T036 Load images into Minikube: `minikube image load todo-backend:local todo-frontend:local` - **SKIPPED: Minikube not installed**
- [ ] T037 Install Helm release: `helm install todo-app ./helm/todo-app -f ./helm/todo-app/values-local.yaml` - **SKIPPED: Minikube not installed**
- [ ] T038 Verify pods reach Running state within 2 minutes per SC-002 - **SKIPPED: Minikube not installed**
- [ ] T039 Verify frontend accessible via `minikube service todo-app-frontend` per SC-003 - **SKIPPED: Minikube not installed**
- [ ] T040 Verify backend health endpoint returns 200 OK per SC-004 - **SKIPPED: Minikube not installed**
- [ ] T041 Verify application functions identically to Phase III per SC-007 - **SKIPPED: Minikube not installed**

### Final Cleanup

- [x] T042 Run final `helm lint ./helm/todo-app` to confirm zero errors/warnings per SC-006 - **PASSED** (1 info warning: icon recommended)
- [x] T043 Document any deployment issues encountered and resolutions - See below

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (US2: Docker Images) ─── BLOCKING ─── Images must exist before deployment
    │
    ▼
Phase 3 (US1+US3: Helm Charts) ─── Helm requires images loaded
    │
    ├──► Phase 4 (US4: AI Docs) ─── Can run in parallel
    │
    └──► Phase 5 (US5: Debug Docs) ─── Can run in parallel
             │
             ▼
         Phase 6 (Validation)
```

### User Story Dependencies

- **US2 (P2)**: No dependencies - can start after Setup
- **US1 (P1)**: Depends on US2 (images must exist)
- **US3 (P3)**: Part of US1 implementation (ConfigMap/Secret in Helm)
- **US4 (P4)**: No dependencies on other stories - documentation only
- **US5 (P5)**: No dependencies on other stories - documentation only

### Parallel Opportunities

**Within Phase 2 (Docker):**
```bash
# Can run in parallel:
T003 backend/.dockerignore
T005 frontend/.dockerignore
```

**Within Phase 3 (Helm):**
```bash
# Backend templates (parallel):
T016 service.yaml
T017 configmap.yaml
T018 secret.yaml

# Frontend templates (parallel):
T023 service.yaml
T024 configmap.yaml

# Helper templates (parallel):
T014 backend/_helpers.tpl
T021 frontend/_helpers.tpl
T012 umbrella/_helpers.tpl
```

**Phases 4 and 5 can run in parallel** since they are documentation verification tasks.

---

## Implementation Strategy

### MVP First (User Stories 2 + 1)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Docker Images (T003-T010)
3. Complete Phase 3: Helm Charts (T011-T028)
4. **STOP and VALIDATE**: Run `helm install` and verify deployment
5. Application should be running on Minikube

### Full Implementation

1. Setup → Docker → Helm → Validate MVP
2. Add US4: AI DevOps Documentation (T029-T031)
3. Add US5: Debug Documentation (T032-T035)
4. Final Validation (T036-T043)

---

## Task Summary

| Phase | Tasks | Parallelizable | Focus |
|-------|-------|----------------|-------|
| 1 | T001-T002 | 1 | Setup |
| 2 | T003-T010 | 2 | Docker Images (US2) |
| 3 | T011-T028 | 10 | Helm Charts (US1, US3) |
| 4 | T029-T031 | 0 | AI Docs (US4) |
| 5 | T032-T035 | 0 | Debug Docs (US5) |
| 6 | T036-T043 | 0 | Validation |

**Total Tasks**: 43
**Tasks per Story**: US1=15, US2=8, US3=4, US4=3, US5=4, Shared=9
**Parallel Opportunities**: 13 tasks marked [P]
**MVP Scope**: Phase 1-3 (T001-T028, 28 tasks)

---

## Notes

- [P] tasks = different files, no dependencies within same phase
- [Story] label maps task to specific user story for traceability
- US1 and US3 combined in Phase 3 since configuration is part of Helm deployment
- Validation phase (6) must wait for real `values-local.yaml` with actual secrets
- No unit tests included - validation is via `helm lint` and deployment verification

---

## T043: Deployment Issues and Resolutions

### Issues Encountered During Docker Build

1. **Poetry 2.x Export Plugin Required**
   - **Issue**: `poetry export` command not found in Poetry 2.x
   - **Resolution**: Updated `backend/Dockerfile` to install `poetry-plugin-export` alongside poetry
   - **File**: `backend/Dockerfile:19`

2. **Better Auth TypeScript Compatibility**
   - **Issue**: `@openai/chatkit` package does not exist on npm
   - **Resolution**: Removed non-existent package from `frontend/package.json`

3. **Better Auth updateUser API Change**
   - **Issue**: `authClient.updateUser()` returns `{ status: boolean }`, not user object
   - **Resolution**: Updated `frontend/src/hooks/use-profile-mutations.ts` to handle correct response type
   - Also updated validation schema to use `name` instead of `email` (Better Auth only supports `name` and `image`)

4. **Broken Import Path**
   - **Issue**: `use-task-stats.ts` imported from `./useAuth` instead of `./use-auth`
   - **Resolution**: Fixed import path in `frontend/src/hooks/use-task-stats.ts`

5. **Missing Public Directory**
   - **Issue**: No `public/` directory existed for Next.js build
   - **Resolution**: Created `frontend/public/.gitkeep` placeholder

6. **Empty Pages Directory Conflict**
   - **Issue**: Empty `src/pages/` directory caused Next.js 16 prerender error
   - **Resolution**: Added `src/pages/` to `frontend/.dockerignore`

### Image Size Exceeded Target

- **Target**: Combined size < 800MB
- **Actual**: Backend (807MB) + Frontend (272MB) = 1,079MB
- **Recommendation**: Consider using Python slim images, removing dev dependencies, or using multi-stage builds with more aggressive cleanup

### Minikube Deployment Skipped

- **Reason**: Minikube not installed on development machine
- **Ready for**: Manual deployment when Minikube is available
- **Images Built**: `todo-backend:local` and `todo-frontend:local` ready for loading

---

## Ready for /sp.implement

All tasks are:
- ✅ Derived strictly from spec.md and plan.md
- ✅ Traceable to functional requirements (FR-001 to FR-024)
- ✅ Granular enough for sequential execution
- ✅ Include exact file paths
- ✅ Organized by user story with clear dependencies
- ✅ MVP identified (Phases 1-3)

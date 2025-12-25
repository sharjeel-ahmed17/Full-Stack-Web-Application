# Implementation Tasks: Task CRUD Operations with Authentication

**Feature Branch**: `001-task-crud-auth`
**Generated**: 2025-12-14
**Total Tasks**: 67
**User Stories**: 7 (mapped from spec.md)

## Task Summary by User Story

| Story | Priority | Tasks | Description |
|-------|----------|-------|-------------|
| Setup | - | 12 | Infrastructure and project scaffolding |
| Foundation | - | 8 | Shared components blocking all stories |
| US1 | P1 | 8 | User Registration |
| US2 | P1 | 7 | User Login |
| US3 | P2 | 8 | View All My Tasks |
| US4 | P2 | 6 | Create New Task |
| US5 | P3 | 6 | Update Task |
| US6 | P3 | 6 | Delete Task |
| US7 | P3 | 6 | Toggle Task Completion |

## Dependency Graph

```
Phase 1: Setup
    ↓
Phase 2: Foundation (Database, Auth deps)
    ↓
┌───────────────────┐
│  US1: Register    │──┐
└───────────────────┘  │
         ↓             │  (P1 - Must complete first)
┌───────────────────┐  │
│  US2: Login       │←─┘
└───────────────────┘
         ↓
┌───────────────────┬───────────────────┐
│  US3: View Tasks  │  US4: Create Task │  (P2 - Can run in parallel)
└───────────────────┴───────────────────┘
         ↓
┌───────────────────┬───────────────────┬───────────────────┐
│  US5: Update      │  US6: Delete      │  US7: Toggle      │  (P3 - Can run in parallel)
└───────────────────┴───────────────────┴───────────────────┘
```

## Parallel Execution Opportunities

| Phase | Parallel Groups | Notes |
|-------|-----------------|-------|
| Setup | T001-T004 (Docker, env) ∥ T005-T008 (Backend scaffold) ∥ T009-T012 (Frontend scaffold) | All independent |
| Foundation | T013-T016 (Backend) ∥ T017-T020 (Frontend) | Backend/Frontend independent |
| US3 + US4 | Entire phases can run in parallel | Different endpoints, different UI |
| US5 + US6 + US7 | Entire phases can run in parallel | Different endpoints, different UI |

---

## Phase 1: Setup (Infrastructure)

**Goal**: Project scaffolding, Docker configuration, environment setup
**Independent Test**: `docker-compose up` starts all 3 services without errors

### Docker & Environment

- [X] T001 [P] Create docker-compose.yml with 3 services (frontend, backend, db) in `docker-compose.yml`
- [X] T002 [P] Create .env.example with all required environment variables in `.env.example`
- [X] T003 [P] Create .gitignore with Python, Node, env, and IDE patterns in `.gitignore`
- [X] T004 [P] Create root README.md with project overview and quickstart in `README.md`

### Backend Scaffolding

- [X] T005 [P] Initialize backend Python project with pyproject.toml in `backend/pyproject.toml`
- [X] T006 [P] Create requirements.txt with FastAPI, SQLModel, Pydantic, Alembic, bcrypt, python-jose in `backend/requirements.txt`
- [X] T007 [P] Create backend Dockerfile with Python 3.13 and UV in `backend/Dockerfile`
- [X] T008 [P] Create backend __init__.py files for package structure in `backend/src/__init__.py`

### Frontend Scaffolding

- [X] T009 [P] Initialize Next.js 16+ project with App Router in `frontend/package.json`
- [X] T010 [P] Configure TypeScript strict mode in `frontend/tsconfig.json`
- [X] T011 [P] Configure Tailwind CSS in `frontend/tailwind.config.ts`
- [X] T012 [P] Create frontend Dockerfile with Node 20 in `frontend/Dockerfile`

---

## Phase 2: Foundation (Blocking Prerequisites)

**Goal**: Shared infrastructure required by all user stories
**Independent Test**: Backend starts with database connection, frontend renders root layout

### Backend Foundation

- [X] T013 Create config.py with Pydantic Settings for environment variables in `backend/src/config.py`
- [X] T014 Create database.py with SQLModel engine and session management in `backend/src/database.py`
- [X] T015 Create FastAPI main.py with CORS, health endpoint, and router mounting in `backend/src/main.py`
- [X] T016 Initialize Alembic with alembic.ini and env.py in `backend/alembic.ini`

### Frontend Foundation

- [X] T017 Create root layout.tsx with HTML structure and Tailwind imports in `frontend/app/layout.tsx`
- [X] T018 Create globals.css with Tailwind directives in `frontend/app/globals.css`
- [X] T019 Create shared TypeScript types matching API contracts in `frontend/types/index.ts`
- [X] T020 Create API client utility with fetch wrapper in `frontend/lib/api.ts`

---

## Phase 3: User Story 1 - User Registration (P1)

**Goal**: Users can create accounts with email/password
**Independent Test**: Submit registration form → account created in database → redirect to login
**Acceptance Criteria**: FR-001 to FR-005, FR-009

### Backend (US1)

- [X] T021 [US1] Create User SQLModel in `backend/src/models/user.py`
- [X] T022 [US1] Create user Pydantic schemas (UserRegisterRequest, UserResponse) in `backend/src/schemas/user.py`
- [X] T023 [US1] Create Alembic migration for users table in `backend/migrations/versions/001_create_users.py`
- [X] T024 [US1] Create auth service with register function (bcrypt hashing) in `backend/src/services/auth.py`
- [X] T025 [US1] Create POST /auth/register endpoint in `backend/src/api/v1/auth.py`

### Frontend (US1)

- [X] T026 [P] [US1] Create reusable Button component in `frontend/components/ui/button.tsx`
- [X] T027 [P] [US1] Create reusable Input component in `frontend/components/ui/input.tsx`
- [X] T028 [US1] Create RegisterForm client component with validation in `frontend/components/auth/register-form.tsx`
- [X] T029 [US1] Create registration page with RegisterForm in `frontend/app/(auth)/register/page.tsx`

---

## Phase 4: User Story 2 - User Login (P1)

**Goal**: Registered users can log in and receive JWT token
**Independent Test**: Submit login form → JWT issued in httpOnly cookie → redirect to dashboard
**Acceptance Criteria**: FR-006 to FR-008, FR-025
**Depends On**: US1 (need registered users)

### Backend (US2)

- [X] T030 [US2] Add login function to auth service (password verification, JWT creation) in `backend/src/services/auth.py`
- [X] T031 [US2] Create POST /auth/login endpoint with cookie setting in `backend/src/api/v1/auth.py`
- [X] T032 [US2] Create get_current_user dependency for JWT validation in `backend/src/api/deps.py`
- [X] T033 [US2] Create GET /auth/me endpoint for current user in `backend/src/api/v1/auth.py`

### Frontend (US2)

- [X] T034 [US2] Configure Better Auth client in `frontend/lib/auth.ts`
- [X] T035 [US2] Create LoginForm client component in `frontend/components/auth/login-form.tsx`
- [X] T036 [US2] Create login page with LoginForm in `frontend/app/(auth)/login/page.tsx`
- [X] T037 [US2] Create auth middleware for protected routes in `frontend/middleware.ts`

---

## Phase 5: User Story 3 - View All My Tasks (P2)

**Goal**: Logged-in users see their tasks sorted by creation date
**Independent Test**: Login → navigate to dashboard → see only own tasks sorted newest first
**Acceptance Criteria**: FR-010 to FR-013, FR-023
**Depends On**: US2 (need authentication)

### Backend (US3)

- [X] T038 [US3] Create Task SQLModel in `backend/src/models/task.py`
- [X] T039 [US3] Create task Pydantic schemas (TaskResponse, TaskListResponse) in `backend/src/schemas/task.py`
- [X] T040 [US3] Create Alembic migration for tasks table in `backend/migrations/versions/002_create_tasks.py`
- [X] T041 [US3] Create task service with list_tasks function (user_id filtering) in `backend/src/services/tasks.py`
- [X] T042 [US3] Create GET /tasks endpoint with pagination in `backend/src/api/v1/tasks.py`

### Frontend (US3)

- [X] T043 [US3] Create EmptyState component for no tasks in `frontend/components/tasks/empty-state.tsx`
- [X] T044 [US3] Create TaskList component (Server Component) in `frontend/components/tasks/task-list.tsx`
- [X] T045 [US3] Create dashboard layout with auth check in `frontend/app/(dashboard)/layout.tsx`
- [X] T046 [US3] Create tasks page with TaskList in `frontend/app/(dashboard)/tasks/page.tsx`

---

## Phase 6: User Story 4 - Create New Task (P2)

**Goal**: Users can create tasks with title and optional description
**Independent Test**: Submit task form → task appears in list → correct user_id and timestamps
**Acceptance Criteria**: FR-014 to FR-017
**Depends On**: US3 (need task list to verify)

### Backend (US4)

- [X] T047 [US4] Create TaskCreateRequest schema in `backend/src/schemas/task.py`
- [X] T048 [US4] Add create_task function to task service in `backend/src/services/tasks.py`
- [X] T049 [US4] Create POST /tasks endpoint in `backend/src/api/v1/tasks.py`

### Frontend (US4)

- [X] T050 [P] [US4] Create Card component for task form container in `frontend/components/ui/card.tsx`
- [X] T051 [US4] Create TaskForm client component for create in `frontend/components/tasks/task-form.tsx`
- [X] T052 [US4] Add create task button and form to tasks page in `frontend/app/(dashboard)/tasks/page.tsx`

---

## Phase 7: User Story 5 - Update Task (P3)

**Goal**: Users can edit task title and description
**Independent Test**: Click edit → modify fields → save → changes persist with updated_at
**Acceptance Criteria**: FR-018
**Depends On**: US4 (need existing tasks)

### Backend (US5)

- [X] T053 [US5] Create TaskUpdateRequest schema in `backend/src/schemas/task.py`
- [X] T054 [US5] Add update_task function to task service (ownership check) in `backend/src/services/tasks.py`
- [X] T055 [US5] Create PUT /tasks/{taskId} endpoint in `backend/src/api/v1/tasks.py`

### Frontend (US5)

- [X] T056 [US5] Add edit mode to TaskForm component in `frontend/components/tasks/task-form.tsx`
- [X] T057 [US5] Create TaskItem component with edit button in `frontend/components/tasks/task-item.tsx`
- [X] T058 [US5] Integrate edit functionality into TaskList in `frontend/components/tasks/task-list.tsx`

---

## Phase 8: User Story 6 - Delete Task (P3)

**Goal**: Users can permanently delete tasks with confirmation
**Independent Test**: Click delete → confirm dialog → task removed from list and database
**Acceptance Criteria**: FR-019, FR-020
**Depends On**: US4 (need existing tasks)

### Backend (US6)

- [X] T059 [US6] Add delete_task function to task service (ownership check) in `backend/src/services/tasks.py`
- [X] T060 [US6] Create DELETE /tasks/{taskId} endpoint in `backend/src/api/v1/tasks.py`

### Frontend (US6)

- [X] T061 [P] [US6] Create Dialog component for confirmation in `frontend/components/ui/dialog.tsx`
- [X] T062 [US6] Add delete button with confirmation to TaskItem in `frontend/components/tasks/task-item.tsx`
- [X] T063 [US6] Handle delete success/error states in TaskList in `frontend/components/tasks/task-list.tsx`

---

## Phase 9: User Story 7 - Toggle Task Completion (P3)

**Goal**: Users can mark tasks complete/incomplete with visual feedback
**Independent Test**: Click checkbox → visual change → is_completed toggled in database
**Acceptance Criteria**: FR-021, FR-022
**Depends On**: US3 (need task list display)

### Backend (US7)

- [X] T064 [US7] Add toggle_completion function to task service in `backend/src/services/tasks.py`
- [X] T065 [US7] Create PATCH /tasks/{taskId}/complete endpoint in `backend/src/api/v1/tasks.py`

### Frontend (US7)

- [X] T066 [US7] Add completion checkbox with strikethrough styling to TaskItem in `frontend/components/tasks/task-item.tsx`
- [X] T067 [US7] Handle optimistic update for toggle in TaskList in `frontend/components/tasks/task-list.tsx`

---

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Error handling, loading states, final integration
**Independent Test**: E2E flow works smoothly with proper feedback

- [X] T068 Add loading spinners to all async operations in `frontend/components/ui/spinner.tsx`
- [X] T069 Add toast notifications for success/error feedback in `frontend/components/ui/toast.tsx`
- [X] T070 Create landing page with login/register links in `frontend/app/page.tsx`
- [X] T071 Add structured logging to backend services in `backend/src/main.py`
- [X] T072 Create auth layout for login/register pages in `frontend/app/(auth)/layout.tsx`

---

## Implementation Strategy

### MVP Scope (Recommended First Delivery)

Complete **Setup + Foundation + US1 + US2** for minimal viable authentication:
- Users can register and login
- JWT authentication working
- Protected routes enforced

### Incremental Delivery Order

1. **Sprint 1**: Setup + Foundation + US1 + US2 (Authentication MVP)
2. **Sprint 2**: US3 + US4 (Task List + Create = Core Functionality)
3. **Sprint 3**: US5 + US6 + US7 (Full CRUD + Polish)

### Parallel Execution Guide

**For 2 developers**:
- Dev A: Backend tasks (T005-T008, T013-T016, backend portions of each US)
- Dev B: Frontend tasks (T009-T012, T017-T020, frontend portions of each US)

**For 3+ developers**:
- After US1+US2 complete, US3 and US4 can be developed in parallel
- After US4 complete, US5, US6, and US7 can be developed in parallel

---

## Independent Test Criteria by Story

| Story | Test Command | Success Criteria |
|-------|--------------|------------------|
| US1 | `POST /auth/register` with valid data | 201 response, user in DB with hashed password |
| US2 | `POST /auth/login` with valid credentials | 200 response, JWT in Set-Cookie header |
| US3 | `GET /tasks` with valid JWT | 200 response, only user's tasks, sorted desc |
| US4 | `POST /tasks` with valid JWT and data | 201 response, task in DB with user_id |
| US5 | `PUT /tasks/{id}` with valid JWT | 200 response, updated_at changed |
| US6 | `DELETE /tasks/{id}` with valid JWT | 204 response, task removed from DB |
| US7 | `PATCH /tasks/{id}/complete` with valid JWT | 200 response, is_completed toggled |

---

## Security Validation Checklist

Execute after all user stories complete:

- [X] T073 Verify all task queries filter by user_id (code review)
- [X] T074 Test cross-user task access returns 404 (not 403)
- [X] T075 Verify passwords are bcrypt hashed (DB inspection)
- [X] T076 Test JWT validation rejects invalid/expired tokens
- [X] T077 Verify httpOnly cookie attributes in browser

---

## References

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Data Model: [data-model.md](./data-model.md)
- API Contract: [contracts/openapi.yaml](./contracts/openapi.yaml)
- ADRs: [history/adr/](../../history/adr/)

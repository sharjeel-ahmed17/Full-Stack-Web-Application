# Research: Task CRUD Operations with Authentication

**Feature Branch**: `001-task-crud-auth`
**Date**: 2025-12-14
**Status**: Complete

## Overview

This document consolidates research findings for the Task CRUD with Authentication feature, resolving all technology decisions based on the Phase II Constitution requirements.

---

## 1. System Architecture

### Decision: Monorepo with Docker Compose Orchestration

**Rationale**: Constitution mandates monorepo structure with `frontend/`, `backend/`, and container orchestration via `docker-compose.yml`. This provides:
- Single repository for coordinated versioning
- Simplified local development with one command startup
- Consistent development/production parity

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Multi-repo | Coordination overhead, version drift, complicates CI/CD |
| Single app (SSR-only) | Constitution requires separate FastAPI backend |

**Structure**:
```
.
├── frontend/         # Next.js 16+ App Router
├── backend/          # FastAPI + SQLModel
├── docker-compose.yml
└── specs/            # Feature specifications
```

---

## 2. Frontend Technology Stack

### Decision: Next.js 16+ with App Router

**Rationale**: Constitution Section III explicitly mandates:
- Next.js 16+ with App Router (NOT Pages Router)
- Server Components by default
- Client Components only with `'use client'` directive
- TypeScript strict mode

**Key Implementation Patterns**:
- Server Components for data fetching (task list, user profile)
- Client Components for interactivity (forms, completion toggle)
- Route handlers for API proxying if needed

### Decision: Tailwind CSS for Styling

**Rationale**: Constitution mandates "Tailwind CSS exclusively" with no inline styles or CSS modules.

### Decision: Better Auth for Frontend Authentication

**Rationale**: Constitution specifies Better Auth with JWT plugin for frontend authentication.

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| NextAuth.js | Not specified in constitution |
| Custom auth | Violates "minimal viable change" principle |

---

## 3. Backend Technology Stack

### Decision: FastAPI + SQLModel + Pydantic v2

**Rationale**: Constitution Section III mandates:
- Python 3.13+
- FastAPI framework
- SQLModel ORM (NOT raw SQLAlchemy)
- Pydantic v2 for validation
- UV package manager

### Decision: Alembic for Database Migrations

**Rationale**: Constitution mandates Alembic for database migrations with SQLModel.

---

## 4. Database Architecture

### Decision: PostgreSQL 16 (Neon Serverless)

**Rationale**: Constitution specifies Neon Serverless PostgreSQL with:
- Connection pooling enabled
- SSL/TLS required for all connections

**Development vs Production**:
| Environment | Database |
|-------------|----------|
| Development | Local PostgreSQL 16 via Docker |
| Production | Neon Serverless PostgreSQL |

### Decision: UUID Primary Keys

**Rationale**: UUIDs provide:
- Global uniqueness across distributed systems
- No sequential ID enumeration vulnerability
- Better suited for multi-tenant applications

---

## 5. Authentication Architecture

### Decision: Better Auth (Frontend) + JWT Verification (Backend)

**Rationale**: Constitution Section III.Authentication specifies:
- Better Auth handles authentication on frontend
- JWT tokens for backend API authentication
- Shared secret (`BETTER_AUTH_SECRET`) between frontend and backend

**Token Configuration** (per Constitution):
- Token expiration: 7 days
- Refresh token rotation enabled
- Password hashing: bcrypt

### Decision: httpOnly Cookies for Token Storage

**Rationale**: Constitution mandates secure cookie attributes:
- HttpOnly (prevents XSS access)
- Secure (HTTPS only in production)
- SameSite (CSRF protection)

**Implementation Flow**:
```
1. User submits credentials to Better Auth (frontend)
2. Better Auth validates, issues JWT + refresh token
3. Tokens stored in httpOnly cookies
4. Frontend sends cookie with API requests
5. Backend validates JWT using shared secret
6. Backend extracts user_id from token for queries
```

---

## 6. Security Implementation

### Decision: User Data Isolation via Mandatory user_id Filtering

**Rationale**: Constitution Section IV (CRITICAL) mandates:
- ALL database queries MUST filter by `user_id`
- No endpoint may return another user's data
- Service layer MUST enforce user context

**Implementation Pattern**:
```python
# CORRECT pattern (per Constitution)
def get_tasks(user_id: UUID) -> list[Task]:
    return db.query(Task).filter(Task.user_id == user_id).all()
```

### Decision: 404 Response for Unauthorized Resource Access

**Rationale**: Spec FR-025 requires generic error messages to prevent user enumeration. Returning 404 (not 403) when a user attempts to access another user's resource prevents confirming the resource exists.

---

## 7. Docker Development Setup

### Decision: 3-Service Docker Compose Configuration

**Services**:
1. **frontend**: Next.js dev server with hot reload
2. **backend**: FastAPI with uvicorn and hot reload
3. **db**: PostgreSQL 16 for local development

**Environment Variables** (via .env):
```
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/todoapp
NEON_DATABASE_URL=<production-neon-url>

# Authentication
BETTER_AUTH_SECRET=<shared-secret>
BETTER_AUTH_URL=http://localhost:3000

# Backend
BACKEND_CORS_ORIGINS=http://localhost:3000
```

**Hot Reload**:
- Frontend: Next.js built-in
- Backend: uvicorn --reload with volume mounts

---

## 8. API Design Decisions

### Decision: RESTful API with OpenAPI Documentation

**Rationale**: Constitution Section VII mandates explicit API contracts with:
- Inputs, outputs, error codes
- Auto-generated OpenAPI/Swagger documentation
- Semantic versioning

**Endpoint Pattern**:
```
GET    /api/v1/tasks          # List user's tasks
POST   /api/v1/tasks          # Create task
GET    /api/v1/tasks/{id}     # Get specific task
PUT    /api/v1/tasks/{id}     # Update task
DELETE /api/v1/tasks/{id}     # Delete task
PATCH  /api/v1/tasks/{id}/complete  # Toggle completion
```

### Decision: Pydantic Schemas for Request/Response Validation

**Rationale**: Constitution mandates Pydantic v2 for runtime validation on both request and response.

---

## 9. Testing Strategy

### Decision: Multi-Layer Testing Approach

**Rationale**: Constitution Section III (Phase II Test Types) requires:

| Test Type | Tool | Purpose |
|-----------|------|---------|
| API Contract Tests | pytest + httpx | Verify OpenAPI compliance |
| Component Tests | Jest + React Testing Library | React component testing |
| E2E User Journey | Playwright | Full user flows |
| Auth Flow Tests | pytest | Login/logout/token refresh |
| User Isolation Tests | pytest | Security boundary testing |

**Coverage Target**: 80% minimum (per Constitution)

---

## 10. Module Structure

### Frontend Structure (App Router):
```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Landing page
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   └── (dashboard)/
│       └── tasks/page.tsx   # Protected task dashboard
├── components/
│   ├── ui/                  # Reusable UI components
│   ├── auth/                # Auth-related components
│   └── tasks/               # Task-related components
├── lib/
│   ├── auth.ts              # Better Auth configuration
│   └── api.ts               # API client
└── types/
    └── index.ts             # Shared TypeScript types
```

### Backend Structure:
```
backend/
├── src/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Configuration management
│   ├── models/
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── schemas/
│   │   ├── user.py          # User Pydantic schemas
│   │   └── task.py          # Task Pydantic schemas
│   ├── api/
│   │   ├── deps.py          # Dependencies (auth, db)
│   │   ├── auth.py          # Auth endpoints
│   │   └── tasks.py         # Task endpoints
│   └── services/
│       ├── auth.py          # Auth business logic
│       └── tasks.py         # Task business logic
├── migrations/              # Alembic migrations
└── tests/
    ├── conftest.py
    ├── test_auth.py
    └── test_tasks.py
```

---

## Critical ADR Decisions Identified

The following architecturally significant decisions should be documented as ADRs:

1. **ADR-001: Better Auth + JWT Shared Secret Architecture**
   - Impact: Authentication security model
   - Alternatives: Session-based, OAuth proxy

2. **ADR-002: User Data Isolation Strategy**
   - Impact: Security model, query patterns
   - Alternatives: Row-level security, tenant databases

3. **ADR-003: Monorepo with Docker Compose**
   - Impact: Development workflow, deployment
   - Alternatives: Multi-repo, serverless

---

## Unresolved Items

**None** - All technical decisions resolved per Constitution requirements.

---

## References

- Constitution v2.0.0: `.specify/memory/constitution.md`
- Feature Specification: `specs/001-task-crud-auth/spec.md`

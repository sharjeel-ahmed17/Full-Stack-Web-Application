# ADR-002: User Data Isolation Architecture

> **Scope**: Documents the security architecture ensuring users can only access their own data, including query patterns, authorization responses, and enforcement layers.

- **Status:** Accepted
- **Date:** 2025-12-14
- **Feature:** 001-task-crud-auth
- **Context:** The todo application is multi-tenant by design—multiple users share the same database tables. Constitution Section IV marks User Data Isolation as CRITICAL, requiring ALL queries to filter by user_id. A security breach allowing cross-user data access would be catastrophic. The architecture must prevent data leakage at multiple layers.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - Core security model
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - RLS, separate DBs
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - All queries, all endpoints -->

## Decision

We adopt a **Service-Layer Enforcement** strategy for user data isolation with the following components:

- **Enforcement Layer**: Service functions (not middleware, not ORM hooks)
- **Query Pattern**: ALL queries MUST include `WHERE user_id = :current_user_id` clause
- **Authorization Response**: Return 404 (not 403) for unauthorized resource access
- **User Context Source**: `user_id` extracted from validated JWT token
- **Dependency Injection**: FastAPI `Depends()` provides current user to endpoints
- **Testing Requirement**: Dedicated `test_isolation.py` with cross-user access tests

**Implementation Pattern**:
```python
# Service layer - ALL queries filter by user_id
async def get_task(db: Session, task_id: UUID, user_id: UUID) -> Task | None:
    """Returns task only if owned by user, else None"""
    return db.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)  # MANDATORY
    ).first()

# API layer - Returns 404 for unauthorized access
@router.get("/tasks/{task_id}")
async def get_task(task_id: UUID, current_user: User = Depends(get_current_user)):
    task = await task_service.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

**Security Principles**:
- **Defense in Depth**: user_id filtering at service layer, not just API layer
- **No Information Leakage**: 404 response doesn't confirm resource existence
- **Explicit Over Implicit**: Every service function requires user_id parameter
- **Test Coverage**: Security boundary tests are mandatory before merge

## Consequences

### Positive

- **Strong Isolation**: Impossible to accidentally return another user's data from service layer
- **Simple Mental Model**: Developers always pass user_id; no hidden magic
- **Testable**: Easy to write tests verifying cross-user access is blocked
- **No External Dependencies**: Works with standard SQLModel/SQLAlchemy
- **Enumeration Prevention**: 404 responses don't leak existence information
- **Constitution Compliant**: Meets CRITICAL requirement from Section IV

### Negative

- **Repetitive Code**: user_id parameter required on every service function
- **Developer Discipline**: Developers must remember to include user_id in queries
- **No Automatic Enforcement**: Unlike RLS, a missed filter is a security bug
- **Query Complexity**: Every query is slightly more complex
- **Test Overhead**: Requires dedicated security tests for each endpoint

## Alternatives Considered

### Alternative A: PostgreSQL Row-Level Security (RLS)
- **Approach**: Database enforces row access based on session variable (current_user_id)
- **Pros**: Automatic enforcement, impossible to bypass at application layer, audit-friendly
- **Cons**: Complex setup, Neon RLS limitations, harder to debug, requires setting session context per request
- **Why Rejected**: Added complexity for MVP; service-layer pattern is simpler and sufficient; Neon serverless connection pooling complicates RLS session variables

### Alternative B: Middleware/ORM Hook Filtering
- **Approach**: Global query hook that automatically adds user_id filter to all Task queries
- **Pros**: Less repetitive code, automatic enforcement
- **Cons**: Magic behavior violates explicitness principle, harder to test, can mask bugs, complex to implement correctly
- **Why Rejected**: Implicit behavior conflicts with Constitution principle IX (Human Intent Over Mechanical Compliance)

### Alternative C: Tenant-Specific Database Schemas
- **Approach**: Each user has their own database schema or separate database
- **Pros**: Complete isolation, simple queries, no filter needed
- **Cons**: Massive operational overhead, doesn't scale, expensive, violates YAGNI
- **Why Rejected**: Extreme over-engineering for a todo app; cost and complexity prohibitive

### Alternative D: API Gateway Authorization
- **Approach**: Authorization checks at API gateway level before reaching backend
- **Pros**: Centralized security, language-agnostic
- **Cons**: Still need service-layer checks (defense in depth), adds infrastructure, latency
- **Why Rejected**: Doesn't replace service-layer isolation; adds complexity without removing need for query filtering

## References

- Feature Spec: [specs/001-task-crud-auth/spec.md](../../specs/001-task-crud-auth/spec.md) (FR-010, FR-018, FR-019)
- Implementation Plan: [specs/001-task-crud-auth/plan.md](../../specs/001-task-crud-auth/plan.md) (Security Checklist)
- Research: [specs/001-task-crud-auth/research.md](../../specs/001-task-crud-auth/research.md) (Section 6)
- Data Model: [specs/001-task-crud-auth/data-model.md](../../specs/001-task-crud-auth/data-model.md) (Security Constraints)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Section IV - CRITICAL)
- Related ADRs: ADR-001 (Authentication provides the user_id)

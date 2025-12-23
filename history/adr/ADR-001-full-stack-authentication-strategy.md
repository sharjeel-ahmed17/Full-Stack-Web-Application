# ADR-001: Full-Stack Authentication Strategy

> **Scope**: Documents the integrated authentication approach spanning frontend (Better Auth), backend (JWT validation), and cross-service token handling.

- **Status:** Accepted
- **Date:** 2025-12-14
- **Feature:** 001-task-crud-auth
- **Context:** Phase II requires user authentication for a multi-tenant todo application where users must only access their own data. The frontend (Next.js) and backend (FastAPI) are separate services requiring a unified authentication strategy that is secure, maintainable, and aligned with Constitution v2.0.0 requirements.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - Defines security model
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Session, OAuth, custom
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - Affects all protected endpoints -->

## Decision

We adopt a **Better Auth + JWT Shared Secret** authentication strategy with the following integrated components:

- **Authentication Library**: Better Auth (frontend-side authentication management)
- **Token Format**: JWT (JSON Web Tokens) for stateless authentication
- **Token Validation**: Shared secret (`BETTER_AUTH_SECRET`) between frontend and backend
- **Token Storage**: httpOnly cookies with Secure and SameSite attributes
- **Password Hashing**: bcrypt with cost factor 10
- **Token Lifecycle**: 7-day expiration with refresh token rotation
- **Backend Verification**: FastAPI dependency that validates JWT and extracts user_id

**Authentication Flow**:
```
1. User submits credentials → Better Auth (frontend)
2. Better Auth validates → Issues JWT + refresh token
3. Tokens stored → httpOnly cookies (prevents XSS)
4. API requests → Cookie sent automatically
5. Backend validates → JWT using shared secret
6. Request authorized → user_id extracted for queries
```

**Security Constraints**:
- Generic error messages for auth failures (prevents user enumeration)
- CORS restricted to frontend origin only
- HTTPS required in production
- Token refresh before expiration

## Consequences

### Positive

- **Stateless Backend**: No session storage required; scales horizontally without sticky sessions
- **Constitution Compliant**: Meets all Phase II authentication requirements
- **XSS Protection**: httpOnly cookies prevent JavaScript access to tokens
- **CSRF Protection**: SameSite cookie attribute mitigates CSRF attacks
- **Simple Validation**: Shared secret allows backend to validate without network calls to auth service
- **Better Auth DX**: Pre-built auth flows, forms, and token management
- **Type Safety**: Better Auth provides TypeScript types for auth state

### Negative

- **Shared Secret Risk**: Secret must be securely managed; if compromised, all tokens can be forged
- **Token Size**: JWTs are larger than session IDs (more bandwidth per request)
- **Revocation Complexity**: Cannot revoke individual JWTs without additional infrastructure (blocklist)
- **Clock Sync**: JWT validation requires synchronized clocks between services
- **Learning Curve**: Team must understand JWT security model and Better Auth patterns

## Alternatives Considered

### Alternative A: Session-Based Authentication
- **Approach**: Server-side sessions stored in Redis/database, session ID in cookie
- **Pros**: Simple revocation, smaller cookies, battle-tested pattern
- **Cons**: Requires shared session store, horizontal scaling complexity, not aligned with Constitution requirement for JWT
- **Why Rejected**: Constitution mandates JWT; session store adds infrastructure complexity

### Alternative B: OAuth2 Proxy Pattern
- **Approach**: Dedicated authentication service (Auth0, Keycloak) handling all auth
- **Pros**: Enterprise features (MFA, SSO), delegated security responsibility
- **Cons**: External dependency, cost, latency on token validation, over-engineering for MVP
- **Why Rejected**: Out of scope for Phase II; adds unnecessary complexity for single-tenant MVP

### Alternative C: Custom JWT Implementation
- **Approach**: Build JWT handling from scratch using jose/jsonwebtoken libraries
- **Pros**: Full control, no library lock-in
- **Cons**: Security risks from implementation errors, reinventing solved problems
- **Why Rejected**: Violates "minimal viable change" principle; Better Auth is battle-tested

## References

- Feature Spec: [specs/001-task-crud-auth/spec.md](../../specs/001-task-crud-auth/spec.md)
- Implementation Plan: [specs/001-task-crud-auth/plan.md](../../specs/001-task-crud-auth/plan.md)
- Research: [specs/001-task-crud-auth/research.md](../../specs/001-task-crud-auth/research.md) (Section 5)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Section III.Authentication)
- Related ADRs: ADR-002 (User Data Isolation depends on user_id from JWT)

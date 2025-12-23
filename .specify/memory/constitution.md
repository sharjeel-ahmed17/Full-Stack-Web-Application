<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 2.0.0 (MAJOR: Phase II technology stack, security, API-first additions)

Modified Principles:
- None renamed; all Phase I principles preserved

Added Sections:
- Section III: Phase II Technology Stack (Frontend, Backend, Authentication subsections)
- Section IV: Phase II Security Requirements (User Data Isolation, Authorization, JWT)
- Section V: API-First Principles (Contract-driven development)
- Updated Test Types for Phase II
- Updated Domain Model with Phase II extensions
- Updated Repository Structure for monorepo

Removed Sections:
- None; Phase II is additive

Templates Status:
- .specify/templates/plan-template.md ✅ Compatible (uses Constitution Check gate)
- .specify/templates/spec-template.md ✅ Compatible (independent test requirement aligned)
- .specify/templates/tasks-template.md ✅ Compatible (multi-app structure supported)
- .specify/templates/phr-template.prompt.md ✅ Compatible (no changes needed)

Follow-up TODOs:
- None; all placeholders resolved
-->

# The Evolution of Todo Constitution

## Preamble

This Constitution establishes the governing principles, standards, and invariants for "The Evolution of Todo" — a multi-phase educational software project demonstrating the evolution of a simple CLI todo application into a cloud-native, AI-powered, event-driven distributed system.

**Core Purpose**: To teach students modern software engineering through Spec-Driven Development (SDD) and AI-assisted implementation, where humans act as architects and AI (Claude Code) performs all coding work.

**Scope of Authority**: This Constitution applies to ALL phases, ALL features, ALL specifications, ALL plans, ALL tasks, and ALL implementations across the entire project lifecycle.

**Supremacy Clause**: If any specification, plan, task, or implementation conflicts with this Constitution, THE CONSTITUTION WINS. The conflicting artifact must be rewritten or regenerated.

**Phase II Context**: This version extends Phase I (In-Memory Python Console App) into a full-stack web application with persistent storage, user authentication, and API-driven architecture. Phase I domain model and principles remain unchanged; Phase II adds web-specific technology governance and security requirements.

## Core Principles

### I. Spec-Driven Development (SDD)

Every feature begins with a complete, testable specification before any implementation work. Specifications MUST define user scenarios, requirements, acceptance criteria, and success metrics. Architects design; Claude Code implements based on specifications, not assumptions. Specifications drive testing, implementation, and validation—never reversed.

### II. Architectural Stewardship by Humans

Humans define architecture, constraints, and design decisions. AI executes implementation according to specification and maintains compliance with this Constitution. Major architectural decisions (framework changes, data model redesigns, deployment strategies, inter-service contracts) require explicit human approval documented as Architecture Decision Records (ADRs). Architecture is non-negotiable; implementation is delegable.

### III. Test-First, Always

Tests MUST be written before implementation. Tests represent the specification contract. Test failure MUST precede implementation. Red-Green-Refactor cycle is mandatory: write failing test → user approves → implement → test passes → refactor if needed. No code ships without passing tests. Unit tests, integration tests, and contract tests are required per feature specification.

### IV. Independent User Story Delivery

Each user story is independently implementable, testable, and deployable. User stories MUST NOT depend on other user stories for core functionality; integration is optional. Each story delivers measurable value. Priority (P1, P2, P3) determines sequencing, not architectural dependency. MVP is the first prioritized story that passes all tests.

### V. Minimal Viable Change

Implementation changes are small, focused, and directly address the specification. No refactoring unrelated code. No "improvements" beyond specification. No premature abstraction. No feature flags for unimplemented features. No backwards-compatibility shims for internal changes. Delete unused code completely. Simplicity is enforced: three identical lines of code is better than a premature utility function.

### VI. Observability & Debuggability

Text-based I/O (stdin/stdout/stderr, logs, JSON) ensures debuggability and auditability. Structured logging with timestamps and context is required. All significant operations MUST be loggable and traceable. Debugging capability is a feature, not optional. No magical behavior; explicit state transitions visible in logs.

### VII. API Contracts & Versioning

Public APIs (CLI, HTTP endpoints, library interfaces) have explicit contracts: inputs, outputs, error codes, timeout/retry semantics. Contracts are versioned. MAJOR.MINOR.PATCH versioning applies to all public-facing changes. Breaking changes require MAJOR version bump and migration documentation. Idempotency, timeouts, and retry strategies are explicit in contracts. Libraries and services versioning is enforced.

### VIII. Simplicity & YAGNI

Start simple. Build only what is specified. Do not design for hypothetical future requirements. Avoid over-engineering. Single responsibility. Explicit over implicit. No unused code. No speculative features. Question complexity in specs; require justification. Simpler solutions are preferred unless specification explicitly requires otherwise.

### IX. Human Intent Over Mechanical Compliance

AI (Claude Code) is bound by specification intent, not mechanical rule-following. When ambiguity exists, clarify with the human architect. Specification intent OVERRIDES template mechanicality. When discovering unspecified dependencies, surface them explicitly—do not assume or guess. Completeness and clarity are prerequisites; incompleteness requires escalation.

## Phase II Technology Stack

### Frontend (Next.js 16+)

**Framework Requirements**:
- MUST use App Router (NOT Pages Router)
- Server Components by default for optimal performance
- Client Components ONLY for interactivity (requires `'use client'` directive)
- TypeScript strict mode enabled (`strict: true` in tsconfig.json)

**Styling**:
- Tailwind CSS exclusively
- NO inline styles
- NO CSS modules
- Consistent utility class usage

**Authentication**:
- Better Auth library with JWT plugin
- Type-safe API client for backend communication
- Token storage in secure HTTP-only cookies

**Dependencies**:
- Package manager: npm or pnpm
- React 18+ (Server Components compatible)
- Next.js 16+

### Backend (FastAPI + SQLModel)

**Runtime Requirements**:
- Python 3.13+ (required)
- UV package manager for dependency management
- Virtual environment isolation

**Framework Stack**:
- FastAPI framework for API endpoints
- SQLModel ORM for database operations (NOT raw SQLAlchemy)
- Pydantic v2 for request/response validation
- Alembic for database migrations

**Database**:
- Neon Serverless PostgreSQL
- Connection pooling enabled
- SSL/TLS required for all connections

**API Standards**:
- OpenAPI/Swagger auto-generated documentation
- JSON request/response format
- Proper HTTP status codes
- Structured error responses

### Authentication (CRITICAL)

**Architecture**:
- Better Auth handles authentication on frontend
- JWT tokens for backend API authentication
- Shared secret (`BETTER_AUTH_SECRET`) between frontend and backend

**Token Configuration**:
- Token expiration: 7 days
- Refresh token rotation enabled
- Password hashing: bcrypt with appropriate cost factor

**Security Requirements**:
- HTTPS required in production
- Secure cookie attributes (HttpOnly, Secure, SameSite)
- CORS properly configured for frontend domain

## Phase II Security Requirements

### User Data Isolation (CRITICAL)

**Mandatory Query Filtering**:
- ALL database queries MUST filter by `user_id`
- No endpoint may return another user's data
- Service layer MUST enforce user context on all operations

**Implementation Pattern**:
```python
# CORRECT: Always filter by user_id
def get_todos(user_id: UUID) -> list[Todo]:
    return db.query(Todo).filter(Todo.user_id == user_id).all()

# WRONG: Never query without user context
def get_todos() -> list[Todo]:
    return db.query(Todo).all()  # SECURITY VIOLATION
```

### Authorization

**URL Parameter Validation**:
- ALWAYS verify `user_id` in URL matches authenticated user
- Reject requests where URL user_id differs from token user_id
- Return 403 Forbidden for authorization failures

**Protected Endpoints**:
- JWT validation required on ALL protected endpoints
- Token must be valid and not expired
- User must exist and be active

### SQL Injection Prevention

**Mandatory Protections**:
- Use SQLModel parameterized queries exclusively
- NEVER construct SQL strings with user input
- NEVER use raw SQL without parameterization

## API-First Principles

### Contract-Driven Development

**Design Order**:
1. API contracts MUST be defined before implementation
2. Backend implements API contract first
3. Frontend consumes contract via type-safe client
4. Integration tests verify contract compliance

**Documentation Requirements**:
- OpenAPI/Swagger documentation auto-generated from code
- All endpoints documented with request/response schemas
- Error responses documented with status codes

**Contract Changes**:
- Breaking changes require ADR documentation
- Semantic versioning for API versions
- Deprecation warnings before removal

### Type Safety

**Frontend-Backend Contract**:
- Shared TypeScript types generated from OpenAPI spec
- Type-safe API client (e.g., openapi-typescript-codegen)
- Runtime validation on both ends

## Development Workflow

### Phase Structure

All features progress through defined phases (Spec → Plan → Tasks → Red → Green → Refactor) documented in the appropriate specification branch and templates. Each phase has clear entry and exit criteria. Phase advancement requires human approval and validation.

### Specification First

Before implementation:
- Feature specification exists at `specs/<feature-id>/spec.md`
- User scenarios are prioritized (P1, P2, P3, etc.)
- Acceptance criteria are testable and measurable
- Success metrics are defined
- Specification is approved by architect

### Implementation Plan

Before coding:
- Implementation plan exists at `specs/<feature-id>/plan.md`
- Technical context (language, dependencies, storage, testing framework) is explicit
- Architecture decisions are documented (or flagged for ADR creation)
- Project structure is defined
- Complexity violations (if any) are justified

### Task Generation & Execution

Tasks are generated from specifications and plans:
- Tasks are granular, specific, and traceable to user stories
- Tasks reference exact file paths
- Task dependencies are explicit
- Tests are included (before implementation)
- Parallel opportunities are marked [P]
- Each user story is independently testable
- Tasks are in `specs/<feature-id>/tasks.md`

### Code Review & Validation

All code changes:
- Reference specifications in commit messages
- Include passing tests (unit, integration, contract as applicable)
- Are reviewed for compliance with this Constitution
- Are traceable to a specification or task
- Meet acceptance criteria before merge

## Quality Gates & Non-Functional Requirements

### Phase II Test Types

**API Integration Tests (Contract Testing)**:
- Verify API endpoints match OpenAPI specification
- Test request/response schema compliance
- Validate error response formats

**Component Tests (React Components)**:
- Test Server Components and Client Components
- Verify component rendering and state
- Test user interactions

**E2E User Journey Tests**:
- Full user flows from frontend through backend
- Authentication flow coverage
- Critical path testing

**Authentication Flow Tests**:
- Login/logout flows
- Token refresh scenarios
- Session expiration handling

**User Isolation Tests (Security Critical)**:
- Verify users cannot access other users' data
- Test authorization boundaries
- Cross-user data leakage prevention

**Coverage Target**: Minimum 80% code coverage across all test types

### Performance & Constraints

Performance requirements, latency targets, throughput targets, and resource constraints MUST be explicit in specification. These are non-functional requirements, not assumptions. If a requirement is not explicit, it is not a requirement.

### Security & Data Handling

- No hardcoded secrets (use .env files)
- Sensitive data handling MUST be explicit in specification
- Authentication and authorization mechanisms MUST be documented in contracts
- All security-related decisions MUST be documented as ADRs
- User data isolation is MANDATORY (see Security Requirements section)

### Observability & Operational Readiness

Logging, metrics, and tracing are built-in, not added later. All significant operations MUST be observable. Runbooks for common operational tasks are required. Deployment and rollback strategies are explicit.

## Domain Model

### Phase I Core (Unchanged)

The following fields from Phase I remain unchanged:
- `id`: Unique identifier for the todo item
- `title`: Title/name of the todo item
- `description`: Optional detailed description
- `completed`: Boolean completion status

### Phase II Extensions (Additive)

Phase II adds the following fields:
- `user_id`: Foreign key to users table (required for multi-user support)
- `created_at`: Timestamp of creation (auto-generated)
- `updated_at`: Timestamp of last modification (auto-updated)

**Migration Note**: Phase II extends Phase I by adding user context and timestamps. All Phase I fields and behaviors remain unchanged to ensure evolutionary consistency.

## Architectural Decision Records (ADRs)

Significant architectural decisions trigger ADR creation:
- **Significant** = impacts system design, future flexibility, or non-functional requirements
- **Examples**: framework selection, data model choices, inter-service communication, caching strategy, authentication approach
- **Process**: Architect detects decision → AI surfaces suggestion → Human approves creation → ADR written and linked
- **Location**: `history/adr/` directory
- **Linking**: ADRs are referenced in specs, plans, and code comments

## Prompt History Records (PHRs)

Every user input that drives development generates a Prompt History Record:
- **Location**: `history/prompts/` organized by stage (constitution, spec, plan, tasks, red, green, refactor, explainer, misc, general)
- **Content**: Verbatim user input + concise assistant response
- **Purpose**: Learning record, traceability, and context preservation
- **Automatic**: Created after every substantive user interaction
- **Never truncated**: Full user input preserved verbatim

## Repository Structure

```
.
├── .specify/
│   ├── memory/
│   │   └── constitution.md        # This file
│   └── templates/
│       ├── spec-template.md
│       ├── plan-template.md
│       ├── tasks-template.md
│       └── commands/
├── specs/
│   ├── 001-feature-name/
│   │   ├── spec.md                # Feature specification
│   │   ├── plan.md                # Implementation plan
│   │   ├── tasks.md               # Task breakdown
│   │   └── research.md            # Research artifacts (optional)
│   └── ...
├── history/
│   ├── prompts/                   # Prompt History Records
│   │   ├── constitution/
│   │   ├── feature-name/
│   │   ├── general/
│   │   └── ...
│   └── adr/                       # Architecture Decision Records
├── frontend/                      # Next.js App
│   ├── CLAUDE.md                  # Frontend-specific guidance
│   ├── app/                       # App Router pages and layouts
│   ├── components/                # React components
│   ├── lib/                       # Utilities and API client
│   └── ...
├── backend/                       # FastAPI App
│   ├── CLAUDE.md                  # Backend-specific guidance
│   ├── src/                       # Source code
│   │   ├── models/                # SQLModel models
│   │   ├── services/              # Business logic
│   │   ├── api/                   # API routes
│   │   └── ...
│   └── tests/                     # Test code
├── docker-compose.yml             # Container orchestration
├── CLAUDE.md                      # Root instructions
└── README.md                      # Project overview
```

## Governance

### Amendment Process

1. User proposes amendment with clear rationale
2. Amendment is reviewed against project purpose and existing principles
3. If approved: Constitution is updated, version is bumped, all dependent templates are validated
4. Conflicting artifacts (specs, plans, tasks) are regenerated or flagged for update
5. PHR records the amendment and rationale

### Version Numbering

- **MAJOR**: Backward-incompatible principle changes, removal of principles, or fundamental scope redefinition
- **MINOR**: New principle added, materially expanded guidance, or new mandatory section
- **PATCH**: Clarifications, wording improvements, typo fixes, or non-semantic refinements
- Current version in footer MUST match the latest amendment date

### Compliance Verification

- All new specifications MUST validate against Constitution before approval
- All plans MUST include "Constitution Check" section identifying compliance or justified violations
- All code MUST be traceable to specifications and MUST respect testing discipline
- ADR suggestions are automatic when architectural decisions are detected

### Agent Guidance

Claude Code (AI agent) operates under this Constitution with the following responsibilities:
- Execute specifications exactly as written
- Flag ambiguities and missing context; do not assume or guess
- Maintain test-first discipline
- Refer to this Constitution when making implementation choices
- Surface ADR suggestions when significant decisions are detected
- Create PHRs automatically after user interactions
- Reject specification changes that violate Constitution principles
- Escalate architectural decisions to human architect
- Enforce user data isolation in all database queries
- Validate JWT tokens on all protected endpoints

---

**Version**: 2.0.0 | **Ratified**: 2025-12-14 | **Last Amended**: 2025-12-14

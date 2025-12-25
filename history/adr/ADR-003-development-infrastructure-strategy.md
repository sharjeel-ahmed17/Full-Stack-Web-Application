# ADR-003: Development Infrastructure Strategy

> **Scope**: Documents the integrated development infrastructure including repository structure, local development environment, and database deployment strategy for development vs production.

- **Status:** Accepted
- **Date:** 2025-12-14
- **Feature:** 001-task-crud-auth
- **Context:** Phase II introduces a full-stack application with frontend (Next.js) and backend (FastAPI) services requiring coordinated development. The team needs a consistent, reproducible development environment that mirrors production while enabling rapid iteration. Constitution mandates specific technology choices (PostgreSQL, Docker) that must be orchestrated effectively.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - Dev workflow, CI/CD
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Multi-repo, serverless
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - All developers, all services -->

## Decision

We adopt a **Monorepo + Docker Compose + Dual Database Deployment** strategy with the following components:

### Repository Structure
- **Pattern**: Monorepo with frontend/ and backend/ directories
- **Rationale**: Coordinated versioning, atomic commits across services, simplified CI/CD

### Local Development Environment
- **Orchestration**: Docker Compose with 3 services
- **Services**:
  - `frontend`: Next.js dev server (port 3000) with hot reload
  - `backend`: FastAPI with uvicorn --reload (port 8000)
  - `db`: PostgreSQL 16 (port 5432)
- **Startup**: Single command (`docker-compose up`)
- **Hot Reload**: Volume mounts for both frontend and backend code

### Database Deployment
| Environment | Database | Connection |
|-------------|----------|------------|
| Development | PostgreSQL 16 (Docker) | `postgresql://postgres:postgres@db:5432/todoapp` |
| Production | Neon Serverless PostgreSQL | `postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require` |

### Environment Configuration
- `.env` file for local secrets (gitignored)
- `.env.example` template committed to repository
- Consistent variable names across environments

**Docker Compose Structure**:
```yaml
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    volumes: ["./frontend:/app"]
    depends_on: [backend]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    volumes: ["./backend:/app"]
    depends_on: [db]
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/todoapp

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=todoapp
      - POSTGRES_PASSWORD=postgres
    volumes: ["pgdata:/var/lib/postgresql/data"]
```

## Consequences

### Positive

- **One Command Startup**: New developers productive in minutes with `docker-compose up`
- **Consistent Environments**: All developers use identical database version and configuration
- **Production Parity**: Local PostgreSQL matches Neon PostgreSQL behavior
- **Atomic Changes**: Frontend and backend changes in single commit/PR
- **Simplified CI/CD**: Single pipeline for entire application
- **Hot Reload**: Rapid iteration without container restarts
- **Offline Development**: Works without internet after initial setup
- **Constitution Compliant**: Meets monorepo and Docker requirements

### Negative

- **Docker Overhead**: Requires Docker Desktop; ~2GB RAM for all services
- **Initial Setup**: Developers must install Docker and understand basics
- **Build Time**: Initial container builds take several minutes
- **Windows Complexity**: Volume mounts can have permission issues on Windows
- **Coupling Risk**: Monorepo can lead to tightly coupled services if not careful
- **Repository Size**: Single repo grows larger over time

## Alternatives Considered

### Alternative A: Multi-Repository Architecture
- **Approach**: Separate repositories for frontend, backend, and infrastructure
- **Pros**: Independent deployments, smaller repositories, team autonomy
- **Cons**: Version coordination complexity, cross-repo changes difficult, multiple CI/CD pipelines
- **Why Rejected**: Constitution mandates monorepo; coordination overhead outweighs benefits for small team

### Alternative B: Cloud-Only Development (No Local Docker)
- **Approach**: Develop against cloud services directly (Neon for DB, deployed preview for testing)
- **Pros**: No local Docker needed, always test against real services
- **Cons**: Requires internet, slower feedback loop, costs for development, environment conflicts
- **Why Rejected**: Offline development valuable; hot reload requires local services; Constitution requires local Docker setup

### Alternative C: Serverless/Edge Development
- **Approach**: Use Vercel/Cloudflare development tools, serverless functions instead of FastAPI
- **Pros**: Zero infrastructure, auto-scaling, edge performance
- **Cons**: Different runtime than production, platform lock-in, Constitution requires FastAPI backend
- **Why Rejected**: Constitution mandates FastAPI; serverless doesn't match production architecture

### Alternative D: Kubernetes Local Development
- **Approach**: Minikube/kind for local Kubernetes matching production
- **Pros**: Production parity if using K8s, advanced orchestration
- **Cons**: Heavy resource requirements, steep learning curve, over-engineering for MVP
- **Why Rejected**: Extreme over-engineering; Docker Compose sufficient for 3-service architecture

## References

- Feature Spec: [specs/001-task-crud-auth/spec.md](../../specs/001-task-crud-auth/spec.md)
- Implementation Plan: [specs/001-task-crud-auth/plan.md](../../specs/001-task-crud-auth/plan.md) (Project Structure)
- Research: [specs/001-task-crud-auth/research.md](../../specs/001-task-crud-auth/research.md) (Sections 1, 4, 7)
- Quickstart Guide: [specs/001-task-crud-auth/quickstart.md](../../specs/001-task-crud-auth/quickstart.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Repository Structure, Section III)
- Related ADRs: ADR-001, ADR-002 (Infrastructure supports auth and data isolation)

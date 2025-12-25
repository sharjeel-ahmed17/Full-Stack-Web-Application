---
id: 001
title: Phase II Constitution Update
stage: constitution
date: 2025-12-14
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: SHARJEELAHMED
command: /sp.constitution
labels: ["constitution", "phase-ii", "technology-stack", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Copy the Phase I constitution from ../In-Memory-Python-Console-App/.specify/memory/constitution.md and update it for Phase II with the following changes:

Core Principles - KEEP AS-IS:

Spec-Driven Development workflow
AI as Primary Developer
Mandatory Traceability (ADR, specs, plans, tasks, PHRs)
Test-First Mandate
Evolutionary Consistency (Phase II extends Phase I)
Technology Governance - UPDATE:

Section III - Add Phase II Stack Requirements:

Frontend (Next.js 16+):

MUST use App Router (NOT Pages Router)
Server Components by default
Client Components only for interactivity ('use client' directive)
TypeScript strict mode
Tailwind CSS (no inline styles, no CSS modules)
Better Auth with JWT plugin
Type-safe API client for backend communication
Backend (FastAPI + SQLModel):

Python 3.13+ (update from 3.10+)
FastAPI framework
SQLModel ORM (NOT raw SQLAlchemy)
Pydantic v2 for validation
UV package manager
Neon Serverless PostgreSQL database
Authentication (CRITICAL):

Better Auth on frontend
JWT tokens for backend auth
Shared secret (BETTER_AUTH_SECRET) between frontend and backend
Token expiration: 7 days
Password hashing with bcrypt
Security - ADD Phase II Requirements:

User Data Isolation: ALL queries MUST filter by user_id
Authorization: ALWAYS verify user_id in URL matches authenticated user
JWT validation on all protected endpoints
No user can access another user's data
SQL injection prevention via SQLModel parameterized queries
Repository Structure - UPDATE for Monorepo: / ├── .specify/memory/constitution.md ├── .spec-kit/config.yaml ├── specs/ ├── history/adr/ ├── history/prompts/ ├── frontend/ # Next.js App │ ├── CLAUDE.md │ ├── app/ # App Router │ ├── components/ │ ├── lib/ │ └── ... ├── backend/ # FastAPI App │ ├── CLAUDE.md │ ├── src/ │ ├── tests/ │ └── ... ├── docker-compose.yml ├── CLAUDE.md # Root instructions └── README.md

Test Types - UPDATE for Phase II:

API Integration Tests (contract testing)
Component Tests (React components)
E2E User Journey Tests
Authentication Flow Tests
User Isolation Tests (security critical)
Minimum 80% coverage target
API-First Principles - ADD:

API contracts MUST be defined before implementation
Backend implements API contract first
Frontend consumes contract via type-safe client
OpenAPI/Swagger documentation auto-generated
Contract breaking changes require ADR
Domain Model - Phase II Extensions (Additive): Add to existing Phase I model:

user_id (foreign key to users table)
created_at, updated_at (timestamps)
All Phase I fields remain unchanged (id, title, description, completed)
Keep all other sections from Phase I constitution unchanged.

## Response snapshot

Created Phase II constitution (v2.0.0) by extending Phase I constitution with:
- Phase II Technology Stack section (Next.js 16+ frontend, FastAPI + SQLModel backend, Better Auth + JWT authentication)
- Phase II Security Requirements section (User Data Isolation, Authorization, SQL Injection Prevention)
- API-First Principles section (Contract-Driven Development, Type Safety)
- Updated Test Types for Phase II (API Integration, Component, E2E, Auth Flow, User Isolation tests with 80% coverage target)
- Updated Domain Model with Phase II extensions (user_id, created_at, updated_at)
- Updated Repository Structure for monorepo (frontend/, backend/ directories)

All 9 core principles from Phase I preserved unchanged. Sync Impact Report included as HTML comment at top of file.

## Outcome

- ✅ Impact: Constitution updated from v1.0.0 to v2.0.0 with Phase II additions
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md (updated)
- 🔁 Next prompts: Feature specification creation, ADR for technology stack decisions
- 🧠 Reflection: MAJOR version bump appropriate due to significant technology stack and security additions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All placeholders resolved, version correct, dates ISO format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A

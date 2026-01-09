# Implementation Plan: AI-Powered Todo Chatbot (Phase 3)

**Branch**: `002-ai-chatbot` | **Date**: 2025-12-26 | **Spec**: [specs/002-ai-chatbot/spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add an AI-powered chatbot interface to the existing Phase 2 full-stack todo application, enabling users to manage tasks via natural language using OpenAI Agents SDK with MCP (Model Context Protocol) tools, integrated with a ChatKit React frontend. The implementation extends the backend with an MCP server layer exposing task operations as tools, configures an OpenAI agent with strict MCP-only enforcement, persists conversation history in the PostgreSQL database, and provides a secure chat API authenticated via existing JWT tokens.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, Pydantic v2, Alembic, OpenAI Agents SDK (NEEDS CLARIFICATION on official package), Official MCP SDK (NEEDS CLARIFICATION on implementation pattern)
- Frontend: Next.js 16+, React 18+, Better Auth, ChatKit React (NEEDS CLARIFICATION on package name and setup)
**Storage**: PostgreSQL 16 (Neon Serverless) - existing database, adding conversation and message tables
**Testing**: pytest (backend), Jest/React Testing Library (frontend), E2E tests for chat flows
**Target Platform**: Web application (existing Next.js frontend + FastAPI backend)
**Project Type**: Web application (monorepo with frontend/ and backend/)
**Performance Goals**:
- Chat response time: <3 seconds end-to-end (spec SC-005)
- Task operation time: <5 seconds from message send to confirmation (spec SC-001)
**Constraints**:
- Zero Phase 2 regression (spec SC-007)
- 100% user data isolation enforcement (spec SC-006)
- Backend-only AI logic and API keys (spec FR-013)
- Stateless API with conversation reconstruction from database (spec FR-016)
**Scale/Scope**:
- Multi-user support (existing auth)
- 90% intent recognition accuracy (spec SC-002)
- 100% MCP tool enforcement (spec SC-003)
- Audit logging for all MCP tool calls (spec SC-010)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development ✅
- Feature specification exists at `specs/002-ai-chatbot/spec.md`
- User scenarios prioritized P1-P3
- Acceptance criteria testable and measurable
- Specification approved by architect

### Architectural Stewardship by Humans ⚠️ NEEDS ADR
- **Significant Decision Detected**: Integration of OpenAI Agents SDK + Official MCP SDK within FastAPI backend
- **Rationale Required**: Choice of agent orchestration pattern, MCP tool registration mechanism, conversation state management strategy
- **Action**: Suggest ADR after Phase 1 design: `/sp.adr openai-agent-mcp-integration-architecture`

### Test-First, Always ✅
- Tests planned before implementation
- Red-Green-Refactor cycle will be followed
- Test types defined: unit (MCP tools), integration (chat API), contract (OpenAI agent tool calling), E2E (chat UI flows)

### Independent User Story Delivery ✅
- User Story 1 (Natural Language Task Creation) - P1: Independently implementable and testable
- User Story 2 (View Tasks via Conversation) - P1: Independent, delivers value
- User Story 3 (Mark Tasks Complete) - P2: Independent
- User Story 4 (Update Task Details) - P3: Independent
- User Story 5 (Delete Tasks) - P3: Independent
- User Story 6 (Conversation History Persistence) - P2: Independent, enhances UX
- All stories deliver measurable value independently

### Minimal Viable Change ✅
- Phase 3 is additive; no refactoring of Phase 2 code
- New backend modules: `src/ai/`, `src/mcp/`, `src/api/v1/chat.py`
- New frontend route: `app/chat/page.tsx`
- New database models: Conversation, Message
- No premature abstractions planned

### Observability & Debuggability ✅
- Structured logging required for all MCP tool calls (spec FR-019)
- Audit trail for agent interactions (spec SC-010)
- Error handling without exposing internals (spec FR-017)

### API Contracts & Versioning ✅
- New endpoint: `POST /api/v1/chat` with explicit input/output contracts
- Error codes documented
- Versioning under `/api/v1/` maintains backward compatibility

### Simplicity & YAGNI ✅
- No deployment infrastructure, no advanced AI features
- Single MCP server reused throughout
- No multi-language support, no voice I/O, no external integrations

### Human Intent Over Mechanical Compliance ✅
- Ambiguities flagged as NEEDS CLARIFICATION in Technical Context
- Research phase (Phase 0) will resolve all unknowns before implementation

### Phase II Technology Stack ✅
- **Frontend**: Next.js 16+ App Router, TypeScript strict mode, Tailwind CSS, Better Auth JWT
- **Backend**: FastAPI, SQLModel, Pydantic v2, Python 3.13+
- **Database**: PostgreSQL 16 (Neon Serverless)
- **Authentication**: JWT tokens, existing Better Auth integration

### Phase II Security Requirements ✅
- **User Data Isolation**: All MCP tools MUST filter by user_id (spec FR-006)
- **Authorization**: JWT validation on `/api/v1/chat` endpoint (spec FR-001, FR-018)
- **SQL Injection Prevention**: SQLModel parameterized queries only
- **API Keys**: OpenAI keys backend-only, never in frontend (spec FR-013)

### API-First Principles ✅
- Chat API contract defined before implementation
- Type-safe frontend client for `/api/v1/chat`
- OpenAPI documentation auto-generated

### Gate Status: ⚠️ PASS WITH CONDITIONS
- All principles aligned ✅
- **Condition 1**: Resolve NEEDS CLARIFICATION items in Phase 0 research
- **Condition 2**: ADR required for OpenAI Agent + MCP integration architecture after Phase 1 design

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── chat-api.openapi.yaml
│   └── mcp-tools.schema.json
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Backend (FastAPI)
backend/
├── src/
│   ├── ai/                         # NEW: AI agent configuration
│   │   ├── __init__.py
│   │   ├── agent.py                # OpenAI agent setup and system prompt
│   │   └── prompts.py              # System prompts enforcing MCP-only behavior
│   ├── mcp/                        # NEW: MCP server and tools
│   │   ├── __init__.py
│   │   ├── server.py               # MCP server initialization
│   │   └── tools/                  # MCP tool definitions
│   │       ├── __init__.py
│   │       ├── add_task.py
│   │       ├── list_tasks.py
│   │       ├── update_task.py
│   │       ├── delete_task.py
│   │       └── complete_task.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py                 # EXISTING
│   │   ├── user.py                 # EXISTING
│   │   ├── conversation.py         # NEW: Conversation model
│   │   └── message.py              # NEW: Message model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py                 # EXISTING
│   │   ├── user.py                 # EXISTING
│   │   └── chat.py                 # NEW: Chat request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── tasks.py                # EXISTING (reused by MCP tools)
│   │   ├── auth.py                 # EXISTING
│   │   └── chat.py                 # NEW: Chat service orchestrating agent + MCP
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                 # EXISTING
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py           # EXISTING (updated to include chat route)
│   │       ├── auth.py             # EXISTING
│   │       ├── tasks.py            # EXISTING
│   │       └── chat.py             # NEW: POST /api/v1/chat endpoint
│   ├── database.py                 # EXISTING
│   ├── config.py                   # EXISTING (add OPENAI_API_KEY env var)
│   └── main.py                     # EXISTING
└── tests/
    ├── unit/
    │   └── mcp/                    # NEW: MCP tool unit tests
    ├── integration/
    │   └── api/
    │       └── test_chat.py        # NEW: Chat API integration tests
    └── e2e/
        └── test_chat_flows.py      # NEW: E2E chat user journey tests

# Frontend (Next.js)
frontend/
├── app/
│   ├── chat/                       # NEW: Chat page
│   │   └── page.tsx
│   ├── tasks/                      # EXISTING
│   ├── layout.tsx                  # EXISTING (add nav link to chat)
│   └── page.tsx                    # EXISTING
├── components/
│   └── chat/                       # NEW: Chat UI components (ChatKit integration)
│       ├── ChatInterface.tsx
│       └── MessageList.tsx
├── lib/
│   ├── api.ts                      # EXISTING (add chatApi client)
│   └── utils.ts                    # EXISTING
└── tests/
    └── components/
        └── chat/                   # NEW: Chat component tests
```

**Structure Decision**: Web application monorepo structure (Option 2 from template). Backend extends existing FastAPI structure with new `ai/` and `mcp/` modules. Frontend adds new `app/chat/` route and `components/chat/` with ChatKit integration. All Phase 2 code remains unchanged.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. Constitution Check passed with conditions (ADR required post-design).

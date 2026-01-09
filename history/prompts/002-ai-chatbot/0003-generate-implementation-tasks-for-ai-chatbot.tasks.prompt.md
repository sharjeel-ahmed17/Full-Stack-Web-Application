---
id: 0003
title: Generate implementation tasks for AI chatbot
stage: tasks
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-ai-chatbot
branch: 002-ai-chatbot
user: SHARJEELAHMED
command: /sp.tasks
labels: ["phase-3", "ai-chatbot", "task-generation", "mcp", "openai-agents"]
links:
  spec: specs/002-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-ai-chatbot/tasks.md
tests:
  - Manual validation per quickstart.md (no automated tests requested)
---

## Prompt

Context:
Phase 2 full-stack todo app (Next.js + FastAPI + Postgres + Auth) is complete.
Task is to implement Phase 3 (AI-powered chatbot) without breaking existing features.

Tasks:

Backend:
1. Create conversation and message database models (user_id, role, content, timestamp).
2. Set up Official MCP SDK inside FastAPI backend.
3. Implement MCP tools:
   - add_task
   - list_tasks
   - update_task
   - delete_task
   - complete_task
   (All tools must require user_id and reuse existing CRUD logic.)
4. Configure OpenAI Agents SDK with a strict system prompt enforcing MCP-only actions.
5. Implement authenticated POST /api/chat endpoint:
   - Verify JWT
   - Load conversation history
   - Run agent with MCP tools
   - Persist messages
   - Return assistant response

Frontend:
6. Add a minimal chat page using ChatKit React.
7. Connect chat UI to /api/chat with JWT attached.
8. Ensure no AI logic or API keys exist on the frontend.

Validation:
9. Test natural language commands for task creation, listing, updating, and completion.
10. Confirm all task operations occur only through MCP tools and are user-scoped.

Goal:
A secure backend-driven AI chatbot that manages todos via natural language using Agent SDK + MCP.

## Response snapshot

Successfully generated tasks.md with 55 tasks organized by user story:

**Phase 1: Setup (3 tasks)** - Install dependencies (openai-agents, mcp, @openai/chatkit-react) and configure OPENAI_API_KEY

**Phase 2: Foundational (9 tasks)** - Database models (Conversation, Message), Alembic migration, MCP infrastructure setup, AI agent configuration, chat schemas

**Phase 3-8: User Stories (25 tasks)** - Organized by priority:
- US1 (P1): Natural language task creation - add_task tool, chat service, /api/v1/chat endpoint
- US2 (P1): View tasks via conversation - list_tasks tool
- US6 (P2): Conversation history persistence - history loading and persistence logic
- US3 (P2): Mark tasks complete - complete_task tool
- US4 (P3): Update task details - update_task tool
- US5 (P3): Delete tasks - delete_task tool

**Phase 9: Frontend (6 tasks)** - ChatKit React components, API client integration, chat page route

**Phase 10: Polish (12 tasks)** - Logging, error handling, security validation, Phase 2 regression testing, quickstart validation

**Key Decisions**:
- Backend-first approach: Complete all MCP tools and chat API before frontend (enables curl testing)
- Tests optional: Manual validation per quickstart.md (not explicitly requested in spec)
- MVP scope: Phases 1-2 + US1, US2, US6 + Frontend (31 tasks)
- 25+ tasks can run in parallel across phases
- User stories are independently implementable and testable

**Dependencies Identified**:
- Foundational phase BLOCKS all user stories
- US3, US4, US5 depend on US2 (need list_tasks for task resolution)
- Frontend depends on at least US1, US2, US6 being complete

## Outcome

- ✅ Impact: Generated comprehensive, immediately executable task list with 55 tasks organized by user story and priority, enabling independent implementation and MVP-first delivery
- 🧪 Tests: Manual validation specified per quickstart.md (automated tests not requested in spec)
- 📁 Files: Created specs/002-ai-chatbot/tasks.md (5.8 KB)
- 🔁 Next prompts: Run /sp.implement to begin execution, or manually start with Phase 1 (Setup) tasks T001-T003
- 🧠 Reflection: Task organization by user story enables parallel development and incremental delivery. Backend-first approach (MCP tools + chat API before frontend) allows comprehensive curl testing before UI work.

## Evaluation notes (flywheel)

- Failure modes observed: None - all design documents were complete and well-structured
- Graders run and results (PASS/FAIL): Format validation PASS - all tasks follow checklist format (checkbox, ID, labels, file paths)
- Prompt variant (if applicable): Standard /sp.tasks workflow with user story organization
- Next experiment (smallest change to try): Consider auto-generating test tasks even when not explicitly requested, then mark as optional

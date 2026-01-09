---
id: 0002
title: Phase 3 AI Chatbot Planning Complete
stage: plan
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-ai-chatbot
branch: 002-ai-chatbot
user: SHARJEELAHMED
command: /sp.plan
labels: ["planning", "ai-chatbot", "phase-3", "openai-agents", "mcp", "chatkit"]
links:
  spec: specs/002-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-ai-chatbot/plan.md
  - specs/002-ai-chatbot/research.md
  - specs/002-ai-chatbot/data-model.md
  - specs/002-ai-chatbot/quickstart.md
  - specs/002-ai-chatbot/contracts/chat-api.openapi.yaml
  - specs/002-ai-chatbot/contracts/mcp-tools.schema.json
  - CLAUDE.md
tests: []
---

## Prompt

Objective:
Upgrade the existing Phase 2 full-stack todo application by adding an AI-powered chatbot using OpenAI Agents SDK, Official MCP SDK, and ChatKit, without breaking existing functionality.

Execution Plan (Phase 3):

1. Preparation
- Freeze existing Phase 2 code (task CRUD + auth).
- Add Phase 3 folder structure in backend (ai/, mcp/, chat API).
- Add database models for conversations and messages.

2. MCP Layer (Backend)
- Set up Official MCP SDK inside FastAPI backend.
- Define and register MCP tools:
  add_task, list_tasks, update_task, delete_task, complete_task.
- Ensure all tools require user_id and reuse existing CRUD logic.

3. AI Agent Layer
- Configure OpenAI Agents SDK.
- Create a restricted system prompt enforcing MCP-only actions.
- Connect the agent to the MCP server for tool execution.

4. Chat API
- Implement POST /api/chat endpoint.
- Authenticate user via JWT.
- Load conversation history from database.
- Run agent with MCP tools.
- Persist user and assistant messages.
- Return final assistant response.

5. Frontend Integration
- Add a minimal chat page using ChatKit React.
- Connect chat UI to /api/chat.
- Ensure JWT is attached automatically.
- No AI logic or secrets on frontend.

6. Validation & Testing
- Test natural language commands for task creation, listing, updating, completion.
- Verify all task changes occur via MCP tools only.
- Confirm multi-user isolation and no Phase 2 regression.

Constraints:
- Backend-first implementation.
- No infrastructure, deployment, or advanced features.
- Single MCP server reused throughout Phase 3.

Outcome:
A secure, AI-powered chatbot that manages user todos via natural language using Agent SDK + MCP, fully integrated into the existing full-stack app.

## Response snapshot

**Planning Complete**: Successfully executed the `/sp.plan` workflow for Phase 3 AI Chatbot feature.

**Artifacts Generated**:
1. **plan.md**: Complete implementation plan with Technical Context, Constitution Check, and Project Structure
2. **research.md**: Resolved all NEEDS CLARIFICATION items:
   - OpenAI Agents SDK: `openai-agents` (v0.6.4+, Python 3.13+ compatible)
   - Official MCP SDK: `mcp` (v1.25.0+, native integration via `agents.mcp`)
   - ChatKit React: `@openai/chatkit-react` (Next.js 16+ compatible)
3. **data-model.md**: Defined Conversation and Message SQLModel models with security requirements
4. **contracts/**: OpenAPI spec for POST /api/v1/chat and MCP tools JSON schema
5. **quickstart.md**: Developer setup guide with troubleshooting and testing workflows
6. **CLAUDE.md**: Updated with Phase 3 technologies in Active Technologies section

**Constitution Check**: ⚠️ PASS WITH CONDITIONS
- All principles aligned ✅
- Condition 1: All NEEDS CLARIFICATION items resolved ✅
- Condition 2: ADR required for OpenAI Agent + MCP integration architecture (flagged for post-design)

**Architecture Decisions**:
- Backend: `openai-agents` + `mcp` with FastMCP for tool registration
- Integration: Native MCP support via `from agents.mcp import MCPServerStdio`
- Frontend: `@openai/chatkit-react` with custom backend integration
- Security: JWT validation + user_id filtering + MCP tool isolation

**Next Steps**:
- Run `/sp.tasks` to generate task breakdown (Phase 2 output)
- Suggest ADR creation: `/sp.adr openai-agent-mcp-integration-architecture`
- Begin implementation following Red-Green-Refactor cycle

## Outcome

- ✅ Impact: Planning phase complete, all design artifacts generated, ready for task breakdown
- 🧪 Tests: None (planning phase, tests will be defined in tasks.md)
- 📁 Files: 7 files created/updated (plan.md, research.md, data-model.md, quickstart.md, 2 contracts, CLAUDE.md)
- 🔁 Next prompts: `/sp.tasks` to generate tasks, `/sp.adr` for ADR creation (optional but recommended)
- 🧠 Reflection: Smooth planning workflow. Research phase resolved all ambiguities via WebSearch. MCP+OpenAI Agents SDK integration is well-documented upstream. ChatKit provides production-grade UI. Constitution Check passed with ADR suggestion flagged. Agent context updated successfully.

## Evaluation notes (flywheel)

- Failure modes observed: None. WebSearch successfully retrieved documentation for all three technologies. Task agents encountered API errors but direct WebSearch succeeded.
- Graders run and results (PASS/FAIL): PASS (all artifacts generated, Constitution Check passed with conditions)
- Prompt variant (if applicable): N/A (standard /sp.plan workflow)
- Next experiment (smallest change to try): Proceed with `/sp.tasks` to validate task breakdown quality

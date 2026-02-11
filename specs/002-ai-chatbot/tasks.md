# Tasks: AI-Powered Todo Chatbot (Phase 3)

**Feature Branch**: `002-ai-chatbot`
**Input**: Design documents from `/specs/002-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Tests**: Not explicitly requested in spec - validation will be manual per quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation for Phase 3

- [ ] T001 Install backend dependencies: uv add openai-agents mcp in backend/
- [ ] T002 [P] Install frontend chat UI dependencies in frontend/
- [ ] T003 [P] Add OPENAI_API_KEY to backend/.env configuration file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database models, MCP infrastructure, and authentication setup that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Models

- [ ] T004 [P] Create Conversation model in backend/src/models/conversation.py with ConversationBase, Conversation, and ConversationRead classes
- [ ] T005 [P] Create Message model with MessageRole enum in backend/src/models/message.py with MessageBase, Message, MessageCreate, and MessageRead classes
- [ ] T006 Generate Alembic migration for conversation and message tables using alembic revision --autogenerate -m "Add conversation and message models"
- [ ] T007 Apply database migration using alembic upgrade head

### MCP Infrastructure

- [ ] T008 [P] Create MCP server initialization module in backend/src/mcp/server.py with FastMCP setup
- [ ] T009 [P] Create MCP tools directory structure: backend/src/mcp/tools/__init__.py

### AI Agent Configuration

- [ ] T010 [P] Create system prompts module in backend/src/ai/prompts.py with strict MCP-only enforcement prompt
- [ ] T011 Create OpenAI agent configuration in backend/src/ai/agent.py with OpenAI Agents SDK setup and MCP integration

### API Schemas

- [ ] T012 [P] Create chat request/response schemas in backend/src/schemas/chat.py with ChatRequest and ChatResponse Pydantic models

**Checkpoint**: Foundation ready - MCP tools and user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create new tasks by typing natural language messages like "Add buy groceries to my tasks"

**Independent Test**: Send a chat message to create a task and verify the task appears in the user's task list via the existing /api/v1/tasks endpoint

### Implementation for User Story 1

- [ ] T013 [P] [US1] Implement add_task MCP tool in backend/src/mcp/tools/add_task.py that accepts user_id, title, description and delegates to existing Task Service
- [ ] T014 [US1] Register add_task tool with MCP server in backend/src/mcp/server.py
- [ ] T015 [US1] Create Chat Service in backend/src/services/chat.py with get_or_create_conversation, load_conversation_history, and persist_message methods
- [ ] T016 [US1] Implement POST /api/v1/chat endpoint in backend/src/api/v1/chat.py with JWT validation, conversation loading, agent execution, and message persistence
- [ ] T017 [US1] Update API router in backend/src/api/v1/router.py to include chat endpoint
- [ ] T018 [US1] Test add_task via curl with natural language message "Add buy groceries to my tasks"

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via chat and verify them in the existing task list

---

## Phase 4: User Story 2 - View Tasks via Conversation (Priority: P1)

**Goal**: Authenticated users can ask natural questions like "what are my tasks?" and receive their task list in conversational format

**Independent Test**: Send a chat message "what are my tasks?" and verify the assistant lists all tasks from the database

### Implementation for User Story 2

- [ ] T019 [P] [US2] Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py that accepts user_id and optional filter_completed, delegates to existing Task Service
- [ ] T020 [US2] Register list_tasks tool with MCP server in backend/src/mcp/server.py
- [ ] T021 [US2] Update agent prompt in backend/src/ai/prompts.py to format task lists conversationally
- [ ] T022 [US2] Test list_tasks via curl with natural language message "what are my tasks?"

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can create and view tasks via chat

---

## Phase 5: User Story 6 - Conversation History Persistence (Priority: P2)

**Goal**: User chat history is stored and loaded automatically across sessions

**Independent Test**: Send multiple messages, refresh the chat page, and verify messages persist on reload

### Implementation for User Story 6

- [ ] T023 [US6] Update Chat Service load_conversation_history method in backend/src/services/chat.py to retrieve last 50 messages ordered by timestamp
- [ ] T024 [US6] Ensure Chat Service persist_message method updates conversation.updated_at timestamp
- [ ] T025 [US6] Test conversation history persistence by sending 5 messages, then loading them via GET /api/v1/chat/history endpoint (if implemented) or by inspecting database

**Checkpoint**: Conversation history now persists - users see their full chat history on page reload

---

## Phase 6: User Story 3 - Mark Tasks as Complete (Priority: P2)

**Goal**: Authenticated users can mark tasks complete by sending messages like "mark buy milk as done"

**Independent Test**: Create a task via chat, mark it complete via chat, verify completion status in database

### Implementation for User Story 3

- [ ] T026 [P] [US3] Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py that accepts user_id and task_id, delegates to existing Task Service
- [ ] T027 [US3] Register complete_task tool with MCP server in backend/src/mcp/server.py
- [ ] T028 [US3] Update agent prompt in backend/src/ai/prompts.py to handle task resolution (call list_tasks first to find task_id by title)
- [ ] T029 [US3] Test complete_task via curl with natural language message "mark buy milk as done"

**Checkpoint**: User Stories 1, 2, 3, and 6 are now functional - users can create, view, and complete tasks via chat with history

---

## Phase 7: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Authenticated users can modify existing tasks through natural language like "change buy milk to buy almond milk"

**Independent Test**: Create a task via chat, update its title via chat, verify the change persists in database

### Implementation for User Story 4

- [ ] T030 [P] [US4] Implement update_task MCP tool in backend/src/mcp/tools/update_task.py that accepts user_id, task_id, optional title and description, delegates to existing Task Service
- [ ] T031 [US4] Register update_task tool with MCP server in backend/src/mcp/server.py
- [ ] T032 [US4] Update agent prompt in backend/src/ai/prompts.py to handle ambiguous update requests and ask for clarification
- [ ] T033 [US4] Test update_task via curl with natural language message "change buy milk to buy almond milk"

**Checkpoint**: User Stories 1-4 and 6 are functional - users can create, view, complete, and update tasks via chat

---

## Phase 8: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Authenticated users can remove tasks by typing messages like "delete buy milk"

**Independent Test**: Create a task via chat, delete it via chat, verify removal from database

### Implementation for User Story 5

- [ ] T034 [P] [US5] Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py that accepts user_id and task_id, delegates to existing Task Service
- [ ] T035 [US5] Register delete_task tool with MCP server in backend/src/mcp/server.py
- [ ] T036 [US5] Update agent prompt in backend/src/ai/prompts.py to handle ambiguous deletion requests and ask for clarification
- [ ] T037 [US5] Test delete_task via curl with natural language message "delete buy milk"

**Checkpoint**: All backend user stories (1-6) are now functional via curl - ready for frontend integration

---

## Phase 9: Frontend Chat Interface

**Purpose**: Build React chat UI using ChatKit to connect to the chat API

### Frontend Components

- [ ] T038 [P] Create ChatInterface component in frontend/components/chat/ChatInterface.tsx with custom chat UI
- [ ] T039 [P] Create MessageList component in frontend/components/chat/MessageList.tsx for displaying conversation history
- [ ] T040 Update API client in frontend/lib/api.ts to add chatApi.sendMessage method with JWT attachment
- [ ] T041 Create chat page route in frontend/app/chat/page.tsx using ChatInterface component
- [ ] T042 [P] Update navigation layout in frontend/app/layout.tsx to add link to /chat route
- [ ] T043 Test chat UI by opening http://localhost:3000/chat, authenticating, and sending test messages

**Checkpoint**: Full-stack chat interface is functional - users can interact with chatbot via UI

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, logging, security validation, and Phase 2 regression testing

### Error Handling & Logging

- [ ] T044 [P] Add structured logging for all MCP tool calls in backend/src/mcp/tools/ with user_id, tool_name, parameters, and results
- [ ] T045 [P] Add error handling in Chat Service in backend/src/services/chat.py to gracefully handle OpenAI API failures and database errors
- [ ] T046 Implement error response formatting in POST /api/v1/chat endpoint to avoid exposing internal errors

### Security Validation

- [ ] T047 [P] Verify user_id isolation: test that User A cannot access User B's tasks via crafted chat prompts
- [ ] T048 [P] Verify JWT validation: test that unauthenticated requests to /api/v1/chat return 401
- [ ] T049 Verify OPENAI_API_KEY is backend-only: inspect frontend code and environment to ensure no API keys are exposed

### Phase 2 Regression Testing

- [ ] T050 [P] Test existing task CRUD APIs (GET, POST, PUT, DELETE /api/v1/tasks) to ensure Phase 2 functionality is unchanged
- [ ] T051 [P] Test existing task UI at http://localhost:3000/tasks to ensure Phase 2 frontend is unchanged
- [ ] T052 Verify database schema: ensure tasks table is unchanged and no existing Phase 2 data is affected

### Documentation & Validation

- [ ] T053 [P] Run quickstart.md validation: follow all steps in specs/002-ai-chatbot/quickstart.md to verify local setup
- [ ] T054 [P] Document edge cases and troubleshooting steps in specs/002-ai-chatbot/quickstart.md if any issues were discovered
- [ ] T055 Update CLAUDE.md to reflect Phase 3 completion status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) OR sequentially in priority order (P1 → P2 → P3)
- **Frontend (Phase 9)**: Depends on at least User Stories 1, 2, and 6 being complete (to have chat API functional)
- **Polish (Phase 10)**: Depends on all user stories and frontend being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (enhances conversation experience)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Requires list_tasks (US2) for task resolution
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Requires list_tasks (US2) for task resolution
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Requires list_tasks (US2) for task resolution

### Within Each User Story

- MCP tools before registration
- Chat service before API endpoint
- Agent configuration before chat service
- Core implementation before testing

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T001 (backend pip install), T002 (frontend npm install), T003 (.env config) can all run in parallel

**Foundational Phase (Phase 2)**:
- T004 (Conversation model), T005 (Message model), T008 (MCP server), T009 (MCP tools dir), T010 (prompts), T012 (schemas) can all run in parallel
- T006 (migration generation) depends on T004, T005
- T007 (migration apply) depends on T006
- T011 (agent config) depends on T010 (prompts)

**User Stories**:
- US1, US2, and US6 can start in parallel after Foundational phase (no inter-story dependencies)
- US3, US4, US5 can start after US2 is complete (they need list_tasks)
- Within each story: Tool implementation (add_task, list_tasks, etc.) can be done in parallel across stories

**Frontend Phase (Phase 9)**:
- T038 (ChatInterface), T039 (MessageList), T040 (API client), T042 (layout update) can run in parallel
- T041 (page route) depends on T038, T039, T040
- T043 (testing) depends on T041

**Polish Phase (Phase 10)**:
- T044 (logging), T045 (error handling), T047-T052 (testing tasks) can all run in parallel
- T053 (quickstart validation), T054 (documentation), T055 (CLAUDE.md update) can run in parallel

---

## Parallel Example: Backend MCP Tools

```bash
# After Foundational phase completes, launch all MCP tools in parallel:
Task T013: "Implement add_task MCP tool in backend/src/mcp/tools/add_task.py"
Task T019: "Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py"
Task T026: "Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py"
Task T030: "Implement update_task MCP tool in backend/src/mcp/tools/update_task.py"
Task T034: "Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py"

# Then register them all sequentially (or in parallel if using code generation):
Task T014, T020, T027, T031, T035: Register tools with MCP server
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 6 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T012) - CRITICAL
3. Complete Phase 3: User Story 1 (T013-T018) - Task creation via chat
4. Complete Phase 4: User Story 2 (T019-T022) - Task viewing via chat
5. Complete Phase 5: User Story 6 (T023-T025) - Conversation history
6. Complete Phase 9: Frontend (T038-T043) - Chat UI
7. **STOP and VALIDATE**: Test all three stories via UI independently
8. Deploy/demo if ready (MVP = create tasks + view tasks + chat history)

### Incremental Delivery

1. **Iteration 1**: Setup + Foundational → Foundation ready
2. **Iteration 2**: Add User Story 1 + 2 + 6 + Frontend → Test independently → **MVP DEPLOYED**
3. **Iteration 3**: Add User Story 3 (complete tasks) → Test independently → Deploy
4. **Iteration 4**: Add User Story 4 + 5 (update/delete tasks) → Test independently → Deploy
5. **Iteration 5**: Polish phase (error handling, security, logging) → Final validation → Deploy

### Parallel Team Strategy

With multiple developers:

1. **Team**: Complete Setup + Foundational together (1-2 days)
2. **Split after Foundational**:
   - **Developer A**: User Story 1 (add_task tool + chat service)
   - **Developer B**: User Story 2 (list_tasks tool + agent prompts)
   - **Developer C**: User Story 6 (conversation history logic)
3. **Converge**: Integrate and test User Stories 1, 2, 6 together
4. **Split again**:
   - **Developer A**: User Story 3 (complete_task)
   - **Developer B**: User Story 4 (update_task)
   - **Developer C**: User Story 5 (delete_task) + Frontend components
5. **Final**: Polish phase together (testing, logging, security)

---

## Success Criteria

**Measurable Outcomes** (from spec.md):

- ✅ SC-001: Task creation via chat in under 5 seconds (test with T018, T022, T029, etc.)
- ✅ SC-002: 90% intent recognition accuracy (manual validation with diverse natural language inputs)
- ✅ SC-003: All task operations use MCP tools (verify by inspecting code - no direct DB access in agent layer)
- ✅ SC-004: Conversation history persists (test with T025)
- ✅ SC-005: Chat interface responds within 3 seconds (test with T043)
- ✅ SC-006: User isolation enforced (test with T047)
- ✅ SC-007: Phase 2 unchanged (test with T050-T052)
- ✅ SC-008: Edge cases handled gracefully (test ambiguous requests, non-existent tasks)
- ✅ SC-009: All core task workflows work via chat (T018, T022, T029, T033, T037)
- ✅ SC-010: MCP tool calls logged with audit trail (verify with T044)

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **Tests**: Not explicitly requested, so validation is manual per quickstart.md
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **Backend-first approach**: Complete all MCP tools and chat API before building frontend (allows curl testing)
- **Security first**: User isolation is critical - test thoroughly with T047

---

**Total Tasks**: 55
**Tasks per User Story**:
- Setup: 3 tasks
- Foundational: 9 tasks (BLOCKING)
- User Story 1 (P1): 6 tasks
- User Story 2 (P1): 4 tasks
- User Story 6 (P2): 3 tasks
- User Story 3 (P2): 4 tasks
- User Story 4 (P3): 4 tasks
- User Story 5 (P3): 4 tasks
- Frontend: 6 tasks
- Polish: 12 tasks

**Suggested MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3-5 (US1, US2, US6) + Phase 9 (Frontend) = 31 tasks

**Parallel Opportunities Identified**: 25+ tasks can run in parallel across different phases

**Format Validation**: ✅ All tasks follow checklist format (checkbox, ID, labels, file paths)

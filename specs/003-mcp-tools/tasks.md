# Tasks: MCP Server & Tools

## Feature Overview

Implementation of stateless Model Context Protocol (MCP) tools for task management operations, integrated with the existing FastAPI backend and SQLModel database layer. The MCP server will expose 5 tools (add_task, list_tasks, complete_task, update_task, delete_task) that operate statelessly and persist data to Neon PostgreSQL, following the existing service patterns for security and user isolation.

## Implementation Strategy

MVP will implement the core add_task and list_tasks functionality first (User Story 1 and 2), allowing basic task creation and retrieval. Subsequent phases will add completion, update, and deletion capabilities. Each user story is designed to be independently testable with clear acceptance criteria.

## Dependencies

User stories can be implemented in parallel after foundational setup is complete, with the exception of User Story 6 (stateless operations) which is cross-cutting and affects all other stories. The implementation order should prioritize P1 stories first (US1, US2, US3) before P2 stories (US4, US5).

## Parallel Execution Examples

- US1 and US2 can be developed in parallel after foundational setup
- US4 and US5 can be developed in parallel after US1, US2, US3 are complete
- MCP tool tests can be written in parallel with tool implementations

---

## Phase 1: Project Setup

Goal: Initialize the MCP server project structure and dependencies

- [ ] T001 Set up MCP directory structure in backend/src/mcp/
- [ ] T002 Install MCP SDK dependency (mcp v1.25.0+) in requirements.txt
- [ ] T003 Create initial MCP server file backend/src/mcp/server.py
- [ ] T004 Create MCP tools directory backend/src/mcp/tools/
- [ ] T005 [P] Create __init__.py files in MCP directories

## Phase 2: Foundational Components

Goal: Implement foundational components needed by all MCP tools

- [ ] T006 Implement MCP tool validators in backend/src/mcp/tools/validators.py
- [ ] T007 Import existing SQLModel services for use in MCP tools
- [ ] T008 Set up database session management for MCP tools
- [ ] T009 Implement basic error handling utilities for MCP tools
- [ ] T010 [P] Set up logging configuration for MCP server (stderr only)

## Phase 3: User Story 1 - Add Task via MCP Tool (Priority: P1)

Goal: Enable creation of new tasks through the add_task MCP tool

Independent Test: Call the add_task MCP tool with valid parameters and verify the task appears in the database.

- [ ] T011 [US1] Create add_task test skeleton in tests/mcp/test_add_task.py
- [ ] T012 [US1] Implement input validation for add_task in validators.py
- [ ] T013 [US1] Create add_task MCP tool implementation in backend/src/mcp/tools/task_operations.py
- [ ] T014 [US1] Integrate add_task with existing create_task service
- [ ] T015 [US1] Add error handling and response formatting for add_task
- [ ] T016 [US1] Write comprehensive tests for add_task in test_add_task.py
- [ ] T017 [US1] Verify add_task meets acceptance scenarios (valid/invalid input)

## Phase 4: User Story 2 - List Tasks via MCP Tool (Priority: P1)

Goal: Enable retrieval of tasks through the list_tasks MCP tool

Independent Test: Call the list_tasks MCP tool and verify it returns a collection of existing tasks.

- [ ] T018 [US2] Create list_tasks test skeleton in tests/mcp/test_list_tasks.py
- [ ] T019 [US2] Implement input validation for list_tasks in validators.py
- [ ] T020 [US2] Create list_tasks MCP tool implementation in backend/src/mcp/tools/task_operations.py
- [ ] T021 [US2] Integrate list_tasks with existing list_user_tasks service
- [ ] T022 [US2] Add pagination support and response formatting for list_tasks
- [ ] T023 [US2] Write comprehensive tests for list_tasks in test_list_tasks.py
- [ ] T024 [US2] Verify list_tasks meets acceptance scenarios (existing/no tasks)

## Phase 5: User Story 3 - Complete Task via MCP Tool (Priority: P1)

Goal: Enable marking tasks as completed through the complete_task MCP tool

Independent Test: Call the complete_task MCP tool with a valid task ID and verify the task's completion status is updated in the database.

- [ ] T025 [US3] Create complete_task test skeleton in tests/mcp/test_complete_task.py
- [ ] T026 [US3] Implement input validation for complete_task in validators.py
- [ ] T027 [US3] Create complete_task MCP tool implementation in backend/src/mcp/tools/task_operations.py
- [ ] T028 [US3] Integrate complete_task with existing update task service
- [ ] T029 [US3] Add status checking and response formatting for complete_task
- [ ] T030 [US3] Write comprehensive tests for complete_task in test_complete_task.py
- [ ] T031 [US3] Verify complete_task meets acceptance scenarios (incomplete/completed tasks)

## Phase 6: User Story 4 - Update Task via MCP Tool (Priority: P2)

Goal: Enable modifying task details through the update_task MCP tool

Independent Test: Call the update_task MCP tool with task ID and new details, then verify the database record is updated.

- [ ] T032 [US4] Create update_task test skeleton in tests/mcp/test_update_task.py
- [ ] T033 [US4] Implement input validation for update_task in validators.py
- [ ] T034 [US4] Create update_task MCP tool implementation in backend/src/mcp/tools/task_operations.py
- [ ] T035 [US4] Integrate update_task with existing update_task service
- [ ] T036 [US4] Add partial update support and response formatting for update_task
- [ ] T037 [US4] Write comprehensive tests for update_task in test_update_task.py
- [ ] T038 [US4] Verify update_task meets acceptance scenarios (existing/non-existent tasks)

## Phase 7: User Story 5 - Delete Task via MCP Tool (Priority: P2)

Goal: Enable removing tasks through the delete_task MCP tool

Independent Test: Call the delete_task MCP tool with a valid task ID and verify the task no longer exists in the database.

- [ ] T039 [US5] Create delete_task test skeleton in tests/mcp/test_delete_task.py
- [ ] T040 [US5] Implement input validation for delete_task in validators.py
- [ ] T041 [US5] Create delete_task MCP tool implementation in backend/src/mcp/tools/task_operations.py
- [ ] T042 [US5] Integrate delete_task with existing delete_task service
- [ ] T043 [US5] Add soft-delete support and response formatting for delete_task
- [ ] T044 [US5] Write comprehensive tests for delete_task in test_delete_task.py
- [ ] T045 [US5] Verify delete_task meets acceptance scenarios (existing/non-existent tasks)

## Phase 8: User Story 6 - Stateless MCP Tool Operations (Priority: P1)

Goal: Ensure all MCP tools operate statelessly with no memory between calls

Independent Test: Call MCP tools in sequence and verify no state is maintained between calls.

- [ ] T046 [US6] Add statelessness verification tests to all MCP tool test files
- [ ] T047 [US6] Ensure all MCP tools use fresh database sessions per call
- [ ] T048 [US6] Verify no global state variables or caching between tool calls
- [ ] T049 [US6] Test concurrent tool execution for independence
- [ ] T050 [US6] Add integration tests for sequential tool usage
- [ ] T051 [US6] Verify all tools pass statelessness acceptance scenarios

## Phase 9: Edge Case Handling

Goal: Handle error conditions and edge cases identified in the specification

- [ ] T052 Implement database connectivity error handling in all tools
- [ ] T053 Add input validation for malformed data in all MCP tools
- [ ] T054 Create tests for non-existent task operations
- [ ] T055 Implement concurrent operation conflict handling
- [ ] T056 Add database resource limit handling
- [ ] T057 Write comprehensive error scenario tests

## Phase 10: Polish & Cross-Cutting Concerns

Goal: Complete the implementation with documentation, final testing, and integration

- [ ] T058 Update main MCP server file to register all tools
- [ ] T059 Add MCP server startup script in backend/
- [ ] T060 Write documentation for MCP server usage in quickstart.md
- [ ] T061 Run full test suite to verify all functionality
- [ ] T062 Perform integration testing with existing backend services
- [ ] T063 Verify all success criteria are met (performance, reliability, etc.)
- [ ] T064 Clean up any debug code and finalize implementation
- [ ] T065 Prepare final delivery artifacts and documentation
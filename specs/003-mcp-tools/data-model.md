# Data Model: MCP Server & Tools

## Core Entities

### Task
**Representation**: Core unit of work in the system
- **id**: UUID (Primary Key) - Unique identifier for the task
- **title**: String - Title/name of the task (required, max 200 chars)
- **description**: String (Optional) - Detailed description of the task
- **is_completed**: Boolean - Completion status of the task
- **user_id**: UUID (Foreign Key) - Owner of the task
- **created_at**: DateTime - Timestamp of creation
- **updated_at**: DateTime - Timestamp of last modification

**Relationships**:
- Belongs to User (many-to-one via user_id)
- User can have multiple tasks (one-to-many)

**Validation Rules**:
- Title is required and must be 1-200 characters
- Description can be empty or up to 1000 characters
- is_completed defaults to False
- All operations require valid user_id for isolation

## MCP Tool Data Flows

### add_task Input Schema
- **user_id**: String (UUID format) - Identifier of the user creating the task
- **title**: String - Title of the task to create
- **description**: String (Optional) - Description of the task

### list_tasks Input Schema
- **user_id**: String (UUID format) - Identifier of the user requesting tasks
- **limit**: Integer (Optional) - Maximum number of tasks to return
- **offset**: Integer (Optional) - Number of tasks to skip (for pagination)

### complete_task Input Schema
- **user_id**: String (UUID format) - Identifier of the user requesting completion
- **task_id**: String (UUID format) - Identifier of the task to complete

### update_task Input Schema
- **user_id**: String (UUID format) - Identifier of the user requesting update
- **task_id**: String (UUID format) - Identifier of the task to update
- **title**: String (Optional) - New title for the task
- **description**: String (Optional) - New description for the task

### delete_task Input Schema
- **user_id**: String (UUID format) - Identifier of the user requesting deletion
- **task_id**: String (UUID format) - Identifier of the task to delete

## State Transitions

### Task States
- **Pending**: New task created with is_completed=False
- **Completed**: Task updated with is_completed=True
- **Deleted**: Task removed from system (via soft delete or hard delete)

### Transition Rules
- Tasks move from Pending → Completed (one-way transition)
- Tasks can be deleted from either state
- All state changes require valid user authentication and authorization
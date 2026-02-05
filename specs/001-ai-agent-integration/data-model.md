# Data Model: AI Agent Integration

## Entities

### Task (Extended from existing model)
- `id`: UUID - Unique identifier for the task
- `title`: String - Title/name of the task
- `description`: String (optional) - Detailed description
- `completed`: Boolean - Completion status
- `user_id`: UUID - Foreign key to users table (required for multi-user support)
- `created_at`: DateTime - Timestamp of creation (auto-generated)
- `updated_at`: DateTime - Timestamp of last modification (auto-updated)

**Validation rules**:
- Title must not be empty
- User_id must reference existing user
- Task cannot be completed before creation

### Conversation
- `id`: UUID - Unique identifier for the conversation
- `user_id`: UUID - Foreign key to users table (owner of conversation)
- `title`: String - Auto-generated title based on conversation content
- `created_at`: DateTime - Timestamp of conversation creation
- `updated_at`: DateTime - Timestamp of last message/activity

**Validation rules**:
- User_id must reference existing user
- Conversation must have at least one message

### Message
- `id`: UUID - Unique identifier for the message
- `conversation_id`: UUID - Foreign key to conversations table
- `role`: String - Role of message sender ('user', 'assistant', 'tool')
- `content`: Text - Content of the message
- `timestamp`: DateTime - When the message was sent/received
- `metadata`: JSON (optional) - Additional metadata (tool calls, AI confidence scores, etc.)

**Validation rules**:
- Conversation_id must reference existing conversation
- Role must be one of allowed values
- Content must not be empty

### AIInteraction
- `id`: UUID - Unique identifier for the interaction
- `conversation_id`: UUID - Foreign key to conversations table
- `tool_name`: String - Name of the MCP tool called
- `input_params`: JSON - Parameters passed to the tool
- `output_result`: JSON - Result returned from the tool
- `timestamp`: DateTime - When the interaction occurred
- `success`: Boolean - Whether the interaction succeeded

**Validation rules**:
- Conversation_id must reference existing conversation
- Tool_name must be valid registered tool
- Success flag must match presence of error in output

## Relationships

- User (1) ←→ (Many) Task
- User (1) ←→ (Many) Conversation
- Conversation (1) ←→ (Many) Message
- Conversation (1) ←→ (Many) AIInteraction

## State Transitions

### Task State Transitions
- Created (completed: false) → Completed (completed: true) → Reopened (completed: false)

### Message State Transitions
- Queued (internal state for pending AI responses) → Sent → Delivered/Read

## Indexes

- Task: user_id, created_at, completed
- Conversation: user_id, updated_at
- Message: conversation_id, timestamp
- AIInteraction: conversation_id, timestamp, tool_name
# Data Model: AI-Powered Todo Chatbot (Phase 3)

**Feature**: 002-ai-chatbot | **Date**: 2025-12-26 | **Phase**: 1 (Design)

## Overview

Phase 3 adds two new database models to support AI chatbot conversations: **Conversation** and **Message**. These models integrate with existing User and Task models from Phase 2.

## Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────────┐         ┌──────────────┐
│   User      │────┬───>│  Conversation    │────┬───>│   Message    │
│ (Phase 2)   │    │    │   (Phase 3)      │    │    │  (Phase 3)   │
└─────────────┘    │    └──────────────────┘    │    └──────────────┘
                   │                             │
                   │    ┌──────────────────┐    │
                   └───>│      Task        │<───┘ (indirect via MCP tools)
                        │   (Phase 2)      │
                        └──────────────────┘
```

**Relationships**:
- User (1) → Conversation (N): One user can have multiple chat conversations
- Conversation (1) → Message (N): One conversation contains multiple messages
- Message belongs to both Conversation and User (for audit/isolation)
- Task is modified indirectly via MCP tools called by AI agent (no direct FK)

---

## Models

### Conversation

**Purpose**: Represents a chat session between a user and the AI chatbot. Tracks metadata about the conversation.

**Table Name**: `conversations`

**Fields**:

| Field        | Type       | Constraints                        | Description                                      |
|--------------|------------|------------------------------------|--------------------------------------------------|
| id           | UUID       | PRIMARY KEY, DEFAULT uuid4()       | Unique identifier for the conversation           |
| user_id      | UUID       | FOREIGN KEY → users.id, NOT NULL, INDEX, ON DELETE CASCADE | Owner of the conversation |
| created_at   | datetime   | NOT NULL, DEFAULT utcnow()         | Timestamp when conversation was created          |
| updated_at   | datetime   | NOT NULL, DEFAULT utcnow()         | Timestamp of last message in conversation        |

**SQLModel Implementation** (backend/src/models/conversation.py):

```python
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey
from typing import Optional


class ConversationBase(SQLModel):
    user_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class ConversationRead(ConversationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
```

**Indexes**:
- Primary Key: `id`
- Foreign Key Index: `user_id` (for efficient user conversation lookups)

**Validation Rules**:
- `user_id` MUST reference an existing user (enforced by FK constraint)
- `updated_at` SHOULD be updated whenever a new message is added (application logic)

**State Transitions**: None (conversations are append-only, no status field)

---

### Message

**Purpose**: Represents a single message in a conversation (user or assistant). Stores message content, role, and timestamp.

**Table Name**: `messages`

**Fields**:

| Field            | Type       | Constraints                                        | Description                                          |
|------------------|------------|----------------------------------------------------|------------------------------------------------------|
| id               | UUID       | PRIMARY KEY, DEFAULT uuid4()                       | Unique identifier for the message                    |
| conversation_id  | UUID       | FOREIGN KEY → conversations.id, NOT NULL, INDEX, ON DELETE CASCADE | Parent conversation |
| user_id          | UUID       | FOREIGN KEY → users.id, NOT NULL, INDEX, ON DELETE CASCADE | Message owner (for audit) |
| role             | str        | ENUM('user', 'assistant'), NOT NULL                | Role of the message sender                           |
| content          | str        | TEXT, NOT NULL                                     | Message text content                                 |
| timestamp        | datetime   | NOT NULL, DEFAULT utcnow()                         | When the message was created                         |

**SQLModel Implementation** (backend/src/models/message.py):

```python
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, Text, Enum as SQLAlchemyEnum
from enum import Enum
from typing import Optional


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    conversation_id: UUID = Field(
        sa_column=Column(
            ForeignKey("conversations.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    user_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    role: MessageRole = Field(
        sa_column=Column(
            SQLAlchemyEnum(MessageRole, native_enum=False),
            nullable=False
        )
    )
    content: str = Field(sa_column=Column(Text, nullable=False))


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(
        sa_column=Column(
            ForeignKey("conversations.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    user_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    role: MessageRole = Field(
        sa_column=Column(
            SQLAlchemyEnum(MessageRole, native_enum=False),
            nullable=False
        )
    )
    content: str = Field(sa_column=Column(Text, nullable=False))
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class MessageCreate(MessageBase):
    content: str


class MessageRead(MessageBase):
    id: UUID
    timestamp: datetime
```

**Indexes**:
- Primary Key: `id`
- Foreign Key Index: `conversation_id` (for efficient message retrieval by conversation)
- Foreign Key Index: `user_id` (for audit and user isolation queries)

**Validation Rules**:
- `conversation_id` MUST reference an existing conversation (enforced by FK)
- `user_id` MUST reference an existing user (enforced by FK)
- `role` MUST be either "user" or "assistant" (enforced by Enum)
- `content` MUST NOT be empty (application validation)
- `user_id` in message MUST match `user_id` of parent conversation (application validation)

**State Transitions**: None (messages are immutable once created)

---

## Existing Models (Phase 2 - Unchanged)

### User

**Table Name**: `users`
**Purpose**: Represents an authenticated user (from Phase 2)

**Relevant Fields**:
- `id` (UUID, PRIMARY KEY)
- `email` (str, UNIQUE, NOT NULL)
- `hashed_password` (str, NOT NULL)
- `created_at` (datetime, NOT NULL)

**No changes required for Phase 3**.

---

### Task

**Table Name**: `tasks`
**Purpose**: Represents a user's todo item (from Phase 2)

**Relevant Fields**:
- `id` (UUID, PRIMARY KEY)
- `user_id` (UUID, FOREIGN KEY → users.id)
- `title` (str, NOT NULL)
- `description` (str, NULLABLE)
- `is_completed` (bool, DEFAULT FALSE)
- `created_at` (datetime, NOT NULL)
- `updated_at` (datetime, NOT NULL)

**No changes required for Phase 3**. Tasks are manipulated via MCP tools (no direct coupling to conversation/message models).

---

## Database Migration

**Migration File**: `backend/alembic/versions/003_add_chat_models.py`

**Up Migration**:
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

CREATE TYPE message_role AS ENUM ('user', 'assistant');

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role message_role NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
```

**Down Migration**:
```sql
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TYPE IF EXISTS message_role;
```

---

## Data Integrity Rules

### User Data Isolation (CRITICAL)

1. **Conversation Isolation**:
   - All conversation queries MUST filter by `user_id`
   - No user can access another user's conversations
   - Enforced at service layer (backend/src/services/chat.py)

2. **Message Isolation**:
   - Messages MUST only be loaded for conversations owned by the authenticated user
   - Message `user_id` MUST match the authenticated user
   - Enforced at service layer and API layer

3. **Task Isolation** (via MCP Tools):
   - MCP tools MUST pass `user_id` to Task Service
   - Task Service filters all queries by `user_id` (existing Phase 2 logic)
   - AI agent CANNOT bypass user isolation via prompt injection

### Referential Integrity

1. **Cascade Deletes**:
   - When a user is deleted, all their conversations and messages are deleted (CASCADE)
   - When a conversation is deleted, all its messages are deleted (CASCADE)

2. **Foreign Key Constraints**:
   - All foreign keys enforced at database level
   - Application MUST handle FK violations gracefully (e.g., user not found → 403)

### Conversation History Constraints

1. **Message Ordering**:
   - Messages loaded in ascending `timestamp` order
   - `timestamp` is immutable (set once on creation)

2. **Conversation State**:
   - `updated_at` on Conversation SHOULD be updated when a message is added
   - Application logic updates `updated_at` after message insert

---

## Query Patterns

### 1. Load Conversation History for Chat API

```python
# Get or create conversation for user
conversation = db.query(Conversation).filter(
    Conversation.user_id == user_id
).order_by(Conversation.updated_at.desc()).first()

if not conversation:
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()

# Load last N messages
messages = db.query(Message).filter(
    Message.conversation_id == conversation.id,
    Message.user_id == user_id  # Redundant but explicit for security
).order_by(Message.timestamp.asc()).limit(50).all()
```

### 2. Persist User Message

```python
user_message = Message(
    conversation_id=conversation.id,
    user_id=user_id,
    role=MessageRole.user,
    content=user_input
)
db.add(user_message)
db.commit()
```

### 3. Persist Assistant Response

```python
assistant_message = Message(
    conversation_id=conversation.id,
    user_id=user_id,  # Same user_id as conversation owner
    role=MessageRole.assistant,
    content=agent_response
)
db.add(assistant_message)

# Update conversation timestamp
conversation.updated_at = datetime.utcnow()
db.commit()
```

---

## Storage Estimates

Assuming:
- Average message size: 200 characters
- Average conversation length: 20 messages
- 1000 active users
- Each user has 5 conversations

**Conversations**: 1000 users × 5 conversations = 5,000 rows (~500 KB)
**Messages**: 5,000 conversations × 20 messages = 100,000 rows (~20 MB for content + metadata)

**Total Phase 3 Storage**: ~25 MB (negligible for PostgreSQL)

---

## Security Notes

1. **No PII in Messages**: User email/password are NOT stored in messages (only user_id FK)
2. **Content Encryption**: Consider encrypting `message.content` at rest (out of scope for Phase 3)
3. **Audit Trail**: All messages are retained for audit purposes (no automatic deletion)
4. **SQL Injection**: SQLModel parameterized queries prevent injection attacks
5. **User Isolation**: Enforced via `user_id` filtering at service layer (Phase 2 pattern extended)

---

## Alembic Migration Command

```bash
# Generate migration
cd backend
alembic revision --autogenerate -m "Add conversation and message models for AI chatbot"

# Apply migration
alembic upgrade head
```

---

## Testing Requirements

1. **Unit Tests**:
   - Conversation model CRUD operations
   - Message model CRUD operations with role enum validation
   - Foreign key constraint enforcement

2. **Integration Tests**:
   - Load conversation history with user_id filtering
   - Persist user and assistant messages
   - Update conversation timestamp on message insert
   - Cascade delete behavior (user deletion → conversations → messages)

3. **Security Tests**:
   - User A cannot load User B's conversations
   - User A cannot insert messages into User B's conversation
   - Invalid role values are rejected

---

**Data Model Complete**: 2025-12-26
**Designer**: Claude Sonnet 4.5 (AI Agent)
**Next Step**: Generate API contracts (contracts/)

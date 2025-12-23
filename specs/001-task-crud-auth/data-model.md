# Data Model: Task CRUD Operations with Authentication

**Feature Branch**: `001-task-crud-auth`
**Date**: 2025-12-14
**ORM**: SQLModel (Python 3.13+)

## Entity Relationship Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│        User         │       │        Task         │
├─────────────────────┤       ├─────────────────────┤
│ id (PK, UUID)       │──┐    │ id (PK, UUID)       │
│ email (UNIQUE)      │  │    │ title (VARCHAR 200) │
│ hashed_password     │  │    │ description (TEXT)  │
│ created_at          │  └───<│ user_id (FK, UUID)  │
│                     │       │ is_completed        │
│                     │       │ created_at          │
│                     │       │ updated_at          │
└─────────────────────┘       └─────────────────────┘
        1                              N
```

---

## Entity: User

### Description
Represents a registered user in the system. Users own tasks and authenticate via email/password.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK, NOT NULL, DEFAULT uuid4() | Unique identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User's email address |
| `hashed_password` | VARCHAR(255) | NOT NULL | bcrypt-hashed password |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | Account creation time |

### SQLModel Definition

```python
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False, index=True)
    )
    hashed_password: str = Field(
        sa_column=Column(String(255), nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| `ix_users_email` | email | UNIQUE B-TREE | Fast email lookup for login |

### Validation Rules (from spec FR-001 to FR-005)

- Email must be valid format (RFC 5322)
- Email must be unique across all users
- Password minimum 8 characters (validated before hashing)
- Password hashed with bcrypt (cost factor 10)

---

## Entity: Task

### Description
Represents a to-do item owned by a user. Tasks have a title, optional description, and completion status.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK, NOT NULL, DEFAULT uuid4() | Unique identifier |
| `title` | VARCHAR(200) | NOT NULL | Task title (1-200 chars) |
| `description` | TEXT | NULLABLE | Optional description (max 1000 chars) |
| `user_id` | UUID | FK → users.id, NOT NULL, INDEX | Owner reference |
| `is_completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | Creation time |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now(), ON UPDATE now() | Last modification |

### SQLModel Definition

```python
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Text, ForeignKey, Boolean

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(
        sa_column=Column(String(200), nullable=False)
    )
    description: str | None = Field(
        default=None,
        sa_column=Column(Text, nullable=True)
    )
    user_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    is_completed: bool = Field(
        default=False,
        sa_column=Column(Boolean, nullable=False, default=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| `ix_tasks_user_id` | user_id | B-TREE | Fast user task lookup |
| `ix_tasks_user_created` | user_id, created_at DESC | COMPOSITE | Optimized task list query |

### Validation Rules (from spec FR-014 to FR-017)

- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- user_id: Required, must reference valid user
- is_completed: Boolean, defaults to FALSE
- created_at: Auto-generated on insert
- updated_at: Auto-updated on any modification

### Cascade Behavior

- ON DELETE CASCADE: When user is deleted, all their tasks are deleted (spec edge case)

---

## Relationships

### User → Task (One-to-Many)

```python
# In User model (optional, for ORM navigation)
tasks: list["Task"] = Relationship(back_populates="owner")

# In Task model (optional, for ORM navigation)
owner: User = Relationship(back_populates="tasks")
```

**Cardinality**: One User has zero or many Tasks. Each Task belongs to exactly one User.

**Enforcement**: Foreign key constraint with CASCADE delete.

---

## Security Constraints

### User Data Isolation (Constitution CRITICAL)

**ALL queries on Task table MUST include user_id filter**:

```python
# CORRECT - Always filter by user_id
def get_user_tasks(db: Session, user_id: UUID) -> list[Task]:
    return db.exec(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    ).all()

# WRONG - Never query without user context
def get_all_tasks(db: Session) -> list[Task]:
    return db.exec(select(Task)).all()  # SECURITY VIOLATION
```

### Authorization Checks

For single-task operations (get, update, delete):

```python
def get_task_for_user(db: Session, task_id: UUID, user_id: UUID) -> Task | None:
    """Returns task only if owned by user, else None (returns 404 to client)"""
    return db.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()
```

---

## State Transitions

### Task Completion State

```
┌──────────────┐    toggle()    ┌──────────────┐
│ is_completed │ ◄────────────► │ is_completed │
│   = false    │                │   = true     │
└──────────────┘                └──────────────┘
```

- Transition: Toggle via PATCH endpoint
- Side effect: `updated_at` timestamp updated
- Authorization: Only task owner can toggle

---

## Migration Strategy

### Initial Migration (Alembic)

```python
# migrations/versions/001_initial_schema.py

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_user_created', 'tasks', ['user_id', 'created_at'])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

---

## Query Patterns

### List Tasks (spec FR-010, FR-011)

```sql
SELECT id, title, description, is_completed, created_at, updated_at
FROM tasks
WHERE user_id = :user_id
ORDER BY created_at DESC
LIMIT 50 OFFSET :offset;
```

### Create Task (spec FR-016, FR-017)

```sql
INSERT INTO tasks (id, title, description, user_id, is_completed, created_at, updated_at)
VALUES (:id, :title, :description, :user_id, false, now(), now())
RETURNING *;
```

### Update Task (spec FR-018)

```sql
UPDATE tasks
SET title = :title, description = :description, updated_at = now()
WHERE id = :task_id AND user_id = :user_id
RETURNING *;
```

### Toggle Completion (spec FR-021)

```sql
UPDATE tasks
SET is_completed = NOT is_completed, updated_at = now()
WHERE id = :task_id AND user_id = :user_id
RETURNING *;
```

### Delete Task (spec FR-019)

```sql
DELETE FROM tasks
WHERE id = :task_id AND user_id = :user_id;
```

---

## References

- Spec FR-001 to FR-025: Functional requirements
- Constitution Section IV: User Data Isolation
- Constitution Section III: SQLModel ORM requirement

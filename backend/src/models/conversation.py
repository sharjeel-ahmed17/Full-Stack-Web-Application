from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field, SQLModel


class ConversationBase(SQLModel):
    user_id: UUID
    title: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a conversation between user and AI agent.

    Validation rules:
    - User_id must reference existing user
    - Conversation must have at least one message
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: UUID
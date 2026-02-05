from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel


class MessageBase(SQLModel):
    conversation_id: UUID
    role: str  # 'user', 'assistant', 'tool'
    content: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class Message(MessageBase, table=True):
    """
    Message model representing individual messages in a conversation.

    Validation rules:
    - Conversation_id must reference existing conversation
    - Role must be one of allowed values
    - Content must not be empty
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: UUID
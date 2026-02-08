from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from sqlalchemy import JSON
import uuid


class Message(SQLModel, table=True):
    """
    Represents an individual message in a conversation, either from user or AI
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)  # Links to parent conversation
    role: str = Field(regex="^(user|assistant)$")  # Identifies the sender (user or assistant)
    content: str = Field(max_length=10000)  # The actual message content (with reasonable limit)
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # When the message was created
    message_metadata: Optional[dict] = Field(default=None, sa_type=JSON)  # Additional message metadata (tool calls, etc.)

    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .message import Message


class Conversation(SQLModel, table=True):
    """
    Represents a chat session between a user and the AI assistant
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)  # Foreign key to user, indexed for performance
    title: Optional[str] = Field(default=None)  # Auto-generated or user-provided title
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")
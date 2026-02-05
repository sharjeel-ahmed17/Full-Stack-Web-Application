from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from ..models.message import Message, MessageCreate


class MessageService:
    """Service for managing messages in AI agent conversations."""

    def create_message(self, session: Session, conversation_id: UUID, role: str, content: str, metadata: Optional[dict] = None) -> Message:
        """Create a new message in a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata=metadata
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def get_message(self, session: Session, message_id: UUID) -> Optional[Message]:
        """Retrieve a message by ID."""
        statement = select(Message).where(Message.id == message_id)
        return session.exec(statement).first()

    def get_messages_by_conversation(self, session: Session, conversation_id: UUID) -> List[Message]:
        """Retrieve all messages in a conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        return session.exec(statement).all()

    def update_message_content(self, session: Session, message_id: UUID, content: str) -> Optional[Message]:
        """Update message content."""
        message = self.get_message(session, message_id)
        if message:
            message.content = content
            session.add(message)
            session.commit()
            session.refresh(message)
        return message
from typing import List
from sqlalchemy.orm import Session
from ..models.message import Message
from ..models.conversation import Conversation
import uuid


def save_message(
    db: Session,
    conversation_id: uuid.UUID,
    role: str,
    content: str,
    message_metadata: dict = None
) -> Message:
    """
    Save a message to a conversation
    """
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        message_metadata=message_metadata
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(db: Session, conversation_id: uuid.UUID) -> List[Message]:
    """
    Get all messages for a conversation
    """
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc()).all()


def get_conversation_history(db: Session, conversation_id: uuid.UUID) -> List[Message]:
    """
    Get the full history of messages in a conversation
    """
    return get_messages(db, conversation_id)


def get_latest_messages(db: Session, conversation_id: uuid.UUID, limit: int = 10) -> List[Message]:
    """
    Get the latest messages from a conversation
    """
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.desc()).limit(limit).all()
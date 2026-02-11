from typing import Optional
from sqlalchemy.orm import Session
from ..models.conversation import Conversation
import uuid


def create_conversation(db: Session, user_id: uuid.UUID, title: Optional[str] = None) -> Conversation:
    """
    Create a new conversation for a user
    """
    conversation = Conversation(
        user_id=user_id,
        title=title
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db: Session, conversation_id: uuid.UUID) -> Optional[Conversation]:
    """
    Get a specific conversation by ID
    """
    return db.get(Conversation, conversation_id)


def get_user_conversation(db: Session, user_id: uuid.UUID) -> Optional[Conversation]:
    """
    Get the active conversation for a user (most recent)
    """
    return db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(Conversation.created_at.desc()).first()


def get_user_conversations(db: Session, user_id: uuid.UUID) -> list[Conversation]:
    """
    Get all conversations for a user
    """
    return db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).all()
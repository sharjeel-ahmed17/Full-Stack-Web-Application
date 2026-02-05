from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message


class ConversationService:
    """Service for managing conversations with AI agents."""

    def create_conversation(self, session: Session, user_id: UUID, title: Optional[str] = None) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_conversation(self, session: Session, conversation_id: UUID) -> Optional[Conversation]:
        """Retrieve a conversation by ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    def get_user_conversations(self, session: Session, user_id: UUID) -> List[Conversation]:
        """Retrieve all conversations for a user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()

    def update_conversation_title(self, session: Session, conversation_id: UUID, title: str) -> Optional[Conversation]:
        """Update conversation title."""
        conversation = self.get_conversation(session, conversation_id)
        if conversation:
            conversation.title = title
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    def get_conversation_messages(self, session: Session, conversation_id: UUID) -> List[Message]:
        """Retrieve all messages in a conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id)
        return session.exec(statement).all()
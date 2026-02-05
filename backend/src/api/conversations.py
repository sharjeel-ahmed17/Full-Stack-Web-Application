from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any, List
from uuid import UUID
import uuid

from ..database import get_session
from ..core.security import get_current_user, TokenData
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", summary="Start a new conversation")
async def start_new_conversation(
    *,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Creates a new conversation session with the AI agent.

    Args:
        session: Database session
        current_user: Current authenticated user

    Returns:
        New conversation ID and creation timestamp
    """
    try:
        conversation_service = ConversationService()

        # Create a new conversation for the user
        conversation = conversation_service.create_conversation(
            session=session,
            user_id=UUID(current_user.user_id)
        )

        return {
            "conversation_id": str(conversation.id),
            "created_at": conversation.created_at.isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating new conversation: {str(e)}"
        )


@router.get("/{conversation_id}", summary="Get conversation history")
async def get_conversation_history(
    conversation_id: str,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Retrieves the full history of a specific conversation.

    Args:
        conversation_id: ID of the conversation to retrieve
        session: Database session
        current_user: Current authenticated user

    Returns:
        Conversation history with all messages
    """
    try:
        # Convert conversation_id string to UUID
        conv_id = UUID(conversation_id)

        conversation_service = ConversationService()
        message_service = MessageService()

        # Verify that the user owns this conversation
        conversation = conversation_service.get_conversation(session, conv_id)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        if str(conversation.user_id) != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't own this conversation"
            )

        # Get all messages in the conversation
        messages = conversation_service.get_conversation_messages(session, conv_id)

        return {
            "conversation": {
                "id": str(conversation.id),
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "messages": [
                    {
                        "id": str(msg.id),
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat()
                    }
                    for msg in messages
                ]
            }
        }

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversation: {str(e)}"
        )


@router.get("/", summary="Get user's conversations")
async def get_user_conversations(
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Retrieves all conversations for the current user.

    Args:
        session: Database session
        current_user: Current authenticated user

    Returns:
        List of user's conversations
    """
    try:
        conversation_service = ConversationService()

        # Get all conversations for the user
        conversations = conversation_service.get_user_conversations(
            session=session,
            user_id=UUID(current_user.user_id)
        )

        return {
            "conversations": [
                {
                    "id": str(conv.id),
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user conversations: {str(e)}"
        )
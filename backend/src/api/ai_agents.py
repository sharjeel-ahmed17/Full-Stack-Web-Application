from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any
from uuid import UUID
import uuid

from ..database import get_session
from ..core.security import get_current_user, TokenData
from ..services.ai_agent_service import AIAgentService
from ..models.conversation import Conversation

router = APIRouter(prefix="/ai-agent", tags=["ai-agent"])


@router.post("/chat", summary="Send message to AI agent")
async def send_message_to_ai_agent(
    *,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user),
    message: str,
    conversation_id: str
) -> Dict[str, Any]:
    """
    Processes natural language input and routes to appropriate MCP tools.

    Args:
        session: Database session
        current_user: Current authenticated user
        message: Natural language message from user
        conversation_id: ID of the conversation to continue

    Returns:
        Response from AI agent with conversation ID and tool calls
    """
    try:
        # Convert conversation_id string to UUID
        conv_id = UUID(conversation_id)

        # Verify that the user owns this conversation
        # For now, we'll just proceed assuming the user has access

        # Initialize the AI agent service
        ai_agent_service = AIAgentService()

        # Process the user message
        result = await ai_agent_service.process_user_message(
            session=session,
            conversation_id=conv_id,
            user_message=message
        )

        return result

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing AI agent request: {str(e)}"
        )


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
        # Initialize the AI agent service
        ai_agent_service = AIAgentService()

        # Create a new conversation
        conversation = await ai_agent_service.create_new_conversation(
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
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import json

from ...database import get_session_dep
from ...models.conversation import Conversation
from ...models.message import Message
from ...services.conversation_service import (
    create_conversation,
    get_conversation,
    get_user_conversation,
    get_user_conversations
)
from ...services.message_service import save_message, get_messages
from ...services.ai_agent_service import process_message, format_conversation_for_ai

router = APIRouter(prefix="", tags=["conversations"])


@router.post("/{user_id}/chat")
def chat_endpoint(
    user_id: UUID,
    message_data: dict,
    db: Session = Depends(get_session_dep)
):
    """
    Handle chat requests from users and return AI-generated responses
    """
    try:
        # Validate the incoming message
        if "message" not in message_data or not message_data["message"].strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content is required"
            )

        message_content = message_data["message"]
        message_metadata = message_data.get("metadata", {})

        # Get or create a conversation for the user
        conversation = get_user_conversation(db, user_id)
        if not conversation:
            conversation = create_conversation(db, user_id, title=f"Conversation with {user_id}")

        # Save the user's message to the conversation
        user_message = save_message(
            db,
            conversation_id=conversation.id,
            role="user",
            content=message_content,
            message_metadata=message_metadata
        )

        # Get the conversation history to provide context to the AI
        conversation_messages = get_messages(db, conversation.id)
        formatted_messages = format_conversation_for_ai(conversation_messages)

        # Process the message with the AI agent
        ai_response = process_message(formatted_messages, str(user_id))

        # Save the AI's response to the conversation
        ai_message = save_message(
            db,
            conversation_id=conversation.id,
            role=ai_response["role"],
            content=ai_response["content"],
            message_metadata={"tool_calls": ai_response.get("tool_calls", [])}
        )

        # Return the response in the required format
        return {
            "conversation_id": str(conversation.id),
            "response": {
                "content": ai_response["content"],
                "role": ai_response["role"]
            },
            "tool_calls": ai_response.get("tool_calls", []),
            "timestamp": ai_message.timestamp.isoformat()
        }

    except ValueError:
        # This catches UUID parsing errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    except Exception as e:
        # Log the error (in a real app, use proper logging)
        print(f"Error in chat endpoint: {str(e)}")

        # Return a generic error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )


@router.get("/{user_id}/conversations")
def get_user_conversations_endpoint(
    user_id: UUID,
    db: Session = Depends(get_session_dep)
):
    """
    Get all conversations for a user
    """
    try:
        conversations = get_user_conversations(db, user_id)
        return [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            }
            for conv in conversations
        ]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )


@router.get("/{user_id}/conversations/{conversation_id}/messages")
def get_conversation_messages(
    user_id: UUID,
    conversation_id: UUID,
    db: Session = Depends(get_session_dep)
):
    """
    Get all messages in a specific conversation
    """
    try:
        # Verify that the conversation belongs to the user
        conversation = get_conversation(db, conversation_id)
        if not conversation or str(conversation.user_id) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or does not belong to user"
            )

        messages = get_messages(db, conversation_id)
        return [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata
            }
            for msg in messages
        ]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
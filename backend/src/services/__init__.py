"""
Services package for the chat endpoint feature.

Contains services for conversation management, message persistence, and AI agent integration.
"""
from .conversation_service import (
    create_conversation,
    get_conversation,
    get_user_conversation,
    get_user_conversations
)
from .message_service import (
    save_message,
    get_messages,
    get_conversation_history,
    get_latest_messages
)
from .ai_agent_service import (
    process_message,
    format_conversation_for_ai
)

__all__ = [
    "create_conversation",
    "get_conversation",
    "get_user_conversation",
    "get_user_conversations",
    "save_message",
    "get_messages",
    "get_conversation_history",
    "get_latest_messages",
    "process_message",
    "format_conversation_for_ai"
]
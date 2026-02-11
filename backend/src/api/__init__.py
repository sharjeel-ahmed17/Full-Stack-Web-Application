"""
API Endpoints for Chat Endpoint Feature

Contains API endpoints for chat functionality and conversation management.
"""
from .v1.conversations import router as conversations_router

__all__ = ["conversations_router"]
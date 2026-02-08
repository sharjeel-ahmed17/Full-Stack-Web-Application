from fastapi import APIRouter

from .auth import auth_router
from .tasks import tasks_router
from .conversations import router as conversations_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
# Include conversations router - paths will be /api/v1/{user_id}/chat per specification
api_router.include_router(conversations_router)
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    user_id: UUID
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int


class TaskToggleResponse(BaseModel):
    id: UUID
    is_completed: bool
    updated_at: datetime

    class Config:
        from_attributes = True
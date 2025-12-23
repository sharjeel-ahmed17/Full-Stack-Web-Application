from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserRegisterRequest(BaseModel):
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: UUID
    email: str
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String
from typing import Optional


class UserBase(SQLModel):
    email: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False, index=True)
    )


class User(UserBase, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False, index=True)
    )
    hashed_password: str = Field(
        sa_column=Column(String(255), nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    created_at: datetime
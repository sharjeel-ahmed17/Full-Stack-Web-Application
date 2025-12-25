"""
Pydantic Schemas for Task CRUD API

These schemas define the request/response contracts for the API.
Generated from OpenAPI specification for implementation reference.

Feature: 001-task-crud-auth
Date: 2025-12-14
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# =============================================================================
# Authentication Schemas
# =============================================================================

class UserRegisterRequest(BaseModel):
    """Request schema for user registration (POST /auth/register)"""
    email: EmailStr = Field(..., max_length=255, description="User's email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User's password (minimum 8 characters)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    )


class UserLoginRequest(BaseModel):
    """Request schema for user login (POST /auth/login)"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    )


class UserResponse(BaseModel):
    """Response schema for user data"""
    id: UUID = Field(..., description="User's unique identifier")
    email: EmailStr = Field(..., description="User's email address")
    created_at: datetime = Field(..., description="Account creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    """Response schema for successful login"""
    user: UserResponse
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


# =============================================================================
# Task Schemas
# =============================================================================

class TaskCreateRequest(BaseModel):
    """Request schema for creating a task (POST /tasks)"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional task description"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }
    )


class TaskUpdateRequest(BaseModel):
    """Request schema for updating a task (PUT /tasks/{taskId})"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional task description"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, cheese"
            }
        }
    )


class TaskResponse(BaseModel):
    """Response schema for task data"""
    id: UUID = Field(..., description="Task's unique identifier")
    title: str = Field(..., description="Task title")
    description: str | None = Field(None, description="Task description")
    is_completed: bool = Field(..., description="Whether the task is completed")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Response schema for task list with pagination"""
    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks for the user")
    limit: int = Field(..., description="Number of tasks returned")
    offset: int = Field(..., description="Offset used for pagination")


# =============================================================================
# Error Schemas
# =============================================================================

class ErrorResponse(BaseModel):
    """Standard error response schema"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    status_code: int = Field(..., description="HTTP status code")


class ValidationErrorDetail(BaseModel):
    """Validation error detail for a single field"""
    field: str = Field(..., description="Field that failed validation")
    message: str = Field(..., description="Validation error message for the field")


class ValidationErrorResponse(BaseModel):
    """Response schema for validation errors"""
    error: str = Field(default="validation_error", description="Error type")
    message: str = Field(..., description="General validation error message")
    details: list[ValidationErrorDetail] = Field(
        default_factory=list,
        description="List of field-specific validation errors"
    )

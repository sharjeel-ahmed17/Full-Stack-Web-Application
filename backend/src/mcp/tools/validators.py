"""
MCP Tool Validators

This module provides input validation utilities for MCP tools to ensure
data integrity and proper formatting before processing.
"""

import re
from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel, validator, ValidationError


class MCPError(Exception):
    """Base exception for MCP operations."""

    def __init__(self, message: str, error_code: str = "GENERIC_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(MCPError):
    """Exception for validation errors."""

    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class DatabaseError(MCPError):
    """Exception for database-related errors."""

    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")


class NotFoundError(MCPError):
    """Exception for when requested resources are not found."""

    def __init__(self, message: str):
        super().__init__(message, "NOT_FOUND_ERROR")


class TaskValidator:
    """Validation utilities for task-related operations."""

    @staticmethod
    def validate_user_id(user_id: str) -> UUID:
        """
        Validate user ID is a proper UUID string.

        Args:
            user_id: String representation of user UUID

        Returns:
            UUID object if valid

        Raises:
            ValueError: If user_id is not a valid UUID
        """
        if not user_id:
            raise ValueError("User ID cannot be empty")

        try:
            uuid_obj = UUID(user_id)
            return uuid_obj
        except ValueError:
            raise ValueError(f"Invalid user ID format: {user_id}. Expected UUID string.")

    @staticmethod
    def validate_task_title(title: str) -> str:
        """
        Validate task title according to business rules.

        Args:
            title: Task title string

        Returns:
            Validated title string

        Raises:
            ValueError: If title doesn't meet requirements
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        title = title.strip()

        if len(title) < 1:
            raise ValueError("Task title must be at least 1 character long")

        if len(title) > 200:
            raise ValueError("Task title must be 200 characters or less")

        return title

    @staticmethod
    def validate_task_description(description: Optional[str]) -> Optional[str]:
        """
        Validate task description according to business rules.

        Args:
            description: Optional task description string

        Returns:
            Validated description string or None

        Raises:
            ValueError: If description doesn't meet requirements
        """
        if description is None:
            return None

        if len(description) > 1000:
            raise ValueError("Task description must be 1000 characters or less")

        return description.strip() if description.strip() else ""

    @staticmethod
    def validate_task_id(task_id: str) -> UUID:
        """
        Validate task ID is a proper UUID string.

        Args:
            task_id: String representation of task UUID

        Returns:
            UUID object if valid

        Raises:
            ValueError: If task_id is not a valid UUID
        """
        if not task_id:
            raise ValueError("Task ID cannot be empty")

        try:
            uuid_obj = UUID(task_id)
            return uuid_obj
        except ValueError:
            raise ValueError(f"Invalid task ID format: {task_id}. Expected UUID string.")

    @staticmethod
    def validate_pagination_params(limit: Optional[int] = None, offset: Optional[int] = None) -> tuple[int, int]:
        """
        Validate pagination parameters for list operations.

        Args:
            limit: Maximum number of items to return (optional)
            offset: Number of items to skip (optional)

        Returns:
            Tuple of (validated limit, validated offset)
        """
        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > 100:
                raise ValueError("Limit must be an integer between 1 and 100")
        else:
            limit = 10  # Default limit

        if offset is not None:
            if not isinstance(offset, int) or offset < 0:
                raise ValueError("Offset must be a non-negative integer")
        else:
            offset = 0  # Default offset

        return limit, offset


class AddTaskInput(BaseModel):
    """Input validation model for add_task operation."""

    user_id: str
    title: str
    description: Optional[str] = None

    @validator('user_id')
    def validate_user_id_format(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError('user_id must be a valid UUID')
        return v

    @validator('title')
    def validate_title_length(cls, v):
        if not v or len(v.strip()) < 1:
            raise ValueError('title must be at least 1 character long')
        if len(v) > 200:
            raise ValueError('title must be 200 characters or less')
        return v.strip()

    @validator('description')
    def validate_description_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('description must be 1000 characters or less')
        return v


class ListTasksInput(BaseModel):
    """Input validation model for list_tasks operation."""

    user_id: str
    limit: Optional[int] = 10
    offset: Optional[int] = 0

    @validator('user_id')
    def validate_user_id_format(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError('user_id must be a valid UUID')
        return v

    @validator('limit')
    def validate_limit(cls, v):
        if v is not None and (v < 1 or v > 100):
            raise ValueError('limit must be between 1 and 100')
        return v

    @validator('offset')
    def validate_offset(cls, v):
        if v is not None and v < 0:
            raise ValueError('offset must be non-negative')
        return v


class CompleteTaskInput(BaseModel):
    """Input validation model for complete_task operation."""

    user_id: str
    task_id: str

    @validator('user_id')
    def validate_user_id_format(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError('user_id must be a valid UUID')
        return v

    @validator('task_id')
    def validate_task_id_format(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError('task_id must be a valid UUID')
        return v


class UpdateTaskInput(BaseModel):
    """Input validation model for update_task operation."""

    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None

    @validator('user_id')
    def validate_user_id_format(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError('user_id must be a valid UUID')
        return v

    @validator('task_id')
    def validate_task_id_format(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError('task_id must be a valid UUID')
        return v

    @validator('title')
    def validate_title_length(cls, v):
        if v is not None:
            if len(v.strip()) < 1:
                raise ValueError('title must be at least 1 character long')
            if len(v) > 200:
                raise ValueError('title must be 200 characters or less')
            return v.strip()
        return v


class DeleteTaskInput(BaseModel):
    """Input validation model for delete_task operation."""

    user_id: str
    task_id: str

    @validator('user_id')
    def validate_user_id_format(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError('user_id must be a valid UUID')
        return v

    @validator('task_id')
    def validate_task_id_format(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError('task_id must be a valid UUID')
        return v
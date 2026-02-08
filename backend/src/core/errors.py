from typing import Optional
from fastapi import HTTPException


class ChatError(HTTPException):
    """Base exception class for chat-related errors"""

    def __init__(self, status_code: int, error: str, message: str, detail: Optional[str] = None):
        super().__init__(
            status_code=status_code,
            detail={
                "error": error,
                "message": message,
                "detail": detail
            }
        )


class InvalidInputError(ChatError):
    """Raised when invalid input is provided to the chat endpoint"""

    def __init__(self, message: str = "Invalid input format", detail: Optional[str] = None):
        super().__init__(
            status_code=400,
            error="Invalid input format",
            message=message,
            detail=detail
        )


class UnauthorizedAccessError(ChatError):
    """Raised when user tries to access resources they don't have permission to access"""

    def __init__(self, message: str = "Access denied", detail: Optional[str] = None):
        super().__init__(
            status_code=403,
            error="Access denied",
            message=message,
            detail=detail
        )


class ResourceNotFoundError(ChatError):
    """Raised when a requested resource is not found"""

    def __init__(self, message: str = "Resource not found", detail: Optional[str] = None):
        super().__init__(
            status_code=404,
            error="Resource not found",
            message=message,
            detail=detail
        )


class ServiceUnavailableError(ChatError):
    """Raised when an external service (like AI service) is unavailable"""

    def __init__(self, message: str = "Service temporarily unavailable", detail: Optional[str] = None):
        super().__init__(
            status_code=503,
            error="Service temporarily unavailable",
            message=message,
            detail=detail
        )
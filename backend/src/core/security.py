from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from ..core.config import settings


# Initialize security schemes
security = HTTPBearer()


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None


def verify_token(token: str) -> TokenData:
    """
    Verify the JWT token and return the token data.

    Args:
        token: The JWT token to verify

    Returns:
        TokenData: The decoded token data containing user information

    Raises:
        HTTPException: If the token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.openai_api_key if settings.openai_api_key else os.getenv("SECRET_KEY", "fallback-secret-key"),
            algorithms=["HS256"]
        )
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")

        if username is None or user_id is None:
            raise credentials_exception

        token_data = TokenData(username=username, user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Get the current user from the token in the request.

    Args:
        credentials: The HTTP authorization credentials from the request

    Returns:
        TokenData: The decoded token data containing user information
    """
    token = credentials.credentials
    return verify_token(token)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new access token.

    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time for the token

    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.openai_api_key if settings.openai_api_key else os.getenv("SECRET_KEY", "fallback-secret-key"),
        algorithm="HS256"
    )

    return encoded_jwt


def validate_ai_input(input_text: str) -> bool:
    """
    Validate AI input for security purposes.

    Args:
        input_text: The input text to validate

    Returns:
        bool: True if the input is valid, False otherwise
    """
    # Check for potentially dangerous patterns
    dangerous_patterns = [
        "DROP TABLE",
        "DELETE FROM",
        "UPDATE ",
        "INSERT INTO",
        "SELECT ",
        "<?php",
        "<script",
        "eval(",
        "exec(",
        "__import__",
        "import subprocess",
        "os.system",
        "subprocess.call"
    ]

    text_upper = input_text.upper()
    for pattern in dangerous_patterns:
        if pattern in text_upper:
            return False

    # Additional validation could include length limits, character set validation, etc.
    if len(input_text) > 10000:  # Arbitrary limit to prevent extremely large inputs
        return False

    return True
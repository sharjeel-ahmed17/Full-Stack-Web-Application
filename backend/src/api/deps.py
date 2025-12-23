from datetime import datetime, timedelta
from uuid import UUID
from typing import Generator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
import bcrypt
from passlib.context import CryptContext
from sqlmodel import Session

from ..config import settings
from ..database import get_session
from ..models.user import User
from ..schemas.user import TokenData

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    """
    with get_session() as session:
        yield session


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current user from the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=UUID(user_id), email=payload.get("email"))
    except JWTError:
        raise credentials_exception

    user = db.get(User, token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
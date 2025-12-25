from sqlmodel import Session
from typing import Optional
from uuid import UUID

from ..models.user import User, UserCreate
from ..api.deps import get_password_hash, verify_password


def register_user(db: Session, user_create: UserCreate) -> User:
    """
    Register a new user with hashed password.
    """
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user by email and password.
    Returns user if credentials are valid, None otherwise.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """
    Get user by ID.
    """
    return db.get(User, user_id)
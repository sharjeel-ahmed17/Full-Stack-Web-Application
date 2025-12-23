from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from uuid import UUID

from ...models.user import User, UserCreate
from ...schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse, TokenResponse
from ...api.deps import get_db, verify_password, get_password_hash, create_access_token, get_current_user
from ...config import settings

auth_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse)
def register(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        created_at=db_user.created_at
    )


@auth_router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint that returns a JWT token.
    """
    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@auth_router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user profile.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at
    )
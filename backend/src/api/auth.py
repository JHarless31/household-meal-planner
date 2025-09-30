"""
Authentication API Routes
Handles user registration, login, logout, and session management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import logging

from src.core.database import get_db
from src.core.security import (
    SecurityManager, get_current_user, set_session_cookie, clear_session_cookie
)
from src.models.user import User
from src.schemas.user import UserCreate, UserLogin, UserResponse
from src.schemas.common import MessageResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    - **username**: Unique username (min 3 characters)
    - **email**: Valid email address
    - **password**: Password (min 8 characters, will be hashed)
    """
    # Check if username already exists
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # Check if email already exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Hash password
    password_hash = SecurityManager.hash_password(user_data.password)

    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        role=user_data.role or "user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"New user registered: {user.username}")
    return user


@router.post("/login")
async def login(
    credentials: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login user and create session.

    Returns session cookie in Set-Cookie header.
    """
    # Find user
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not SecurityManager.verify_password(credentials.password, user.password_hash):
        # Rate limiting would be implemented here in production
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create JWT token
    token = SecurityManager.create_access_token({"user_id": str(user.id)})

    # Create session in database
    SecurityManager.create_session(db, user.id, token)

    # Update last login
    user.last_login = datetime.now()
    db.commit()

    # Set session cookie
    set_session_cookie(response, token)

    logger.info(f"User logged in: {user.username}")

    return {
        "user": UserResponse.model_validate(user),
        "message": "Login successful"
    }


@router.post("/logout", response_model=MessageResponse)
async def logout(
    response: Response,
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    """
    Logout user and end session.

    Clears session cookie and removes session from database.
    """
    if session:
        SecurityManager.delete_session(db, session)

    clear_session_cookie(response)

    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get currently authenticated user information.

    Requires valid session cookie.
    """
    return current_user

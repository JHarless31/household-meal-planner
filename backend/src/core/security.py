"""
Security Module
Handles authentication, JWT tokens, password hashing, and session management
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
import bcrypt
import hashlib
from fastapi import HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session

from src.core.config import settings
from src.models.user import User, Session as UserSession


class SecurityManager:
    """Handles authentication and security operations"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password to verify against

        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.

        Args:
            data: Data to encode in the token
            expires_delta: Optional custom expiration time

        Returns:
            str: JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token to verify

        Returns:
            Optional[Dict]: Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def hash_token(token: str) -> str:
        """
        Hash a token for secure storage.

        Args:
            token: Token to hash

        Returns:
            str: Hashed token
        """
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def create_session(
        db: Session,
        user_id: str,
        token: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> UserSession:
        """
        Create a new session in the database.

        Args:
            db: Database session
            user_id: User identifier
            token: JWT token
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            UserSession: Created session object
        """
        token_hash = SecurityManager.hash_token(token)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

        session = UserSession(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_session(db: Session, token: str) -> Optional[UserSession]:
        """
        Get session by token.

        Args:
            db: Database session
            token: JWT token

        Returns:
            Optional[UserSession]: Session object or None if not found
        """
        token_hash = SecurityManager.hash_token(token)
        session = db.query(UserSession).filter(
            UserSession.token_hash == token_hash,
            UserSession.expires_at > datetime.now(timezone.utc)
        ).first()

        if session:
            # Update last accessed time
            session.last_accessed = datetime.now(timezone.utc)
            db.commit()

        return session

    @staticmethod
    def delete_session(db: Session, token: str) -> bool:
        """
        Delete a session (logout).

        Args:
            db: Database session
            token: JWT token

        Returns:
            bool: True if session was deleted, False otherwise
        """
        token_hash = SecurityManager.hash_token(token)
        session = db.query(UserSession).filter(UserSession.token_hash == token_hash).first()
        if session:
            db.delete(session)
            db.commit()
            return True
        return False

    @staticmethod
    def cleanup_expired_sessions(db: Session) -> int:
        """
        Remove expired sessions from database.

        Args:
            db: Database session

        Returns:
            int: Number of sessions deleted
        """
        count = db.query(UserSession).filter(
            UserSession.expires_at <= datetime.now(timezone.utc)
        ).delete()
        db.commit()
        return count


def get_current_user(
    db: Session,
    session: Optional[str] = Cookie(None)
) -> User:
    """
    Dependency to get current authenticated user from session cookie.

    Args:
        db: Database session
        session: Session cookie value

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Verify token
    payload = SecurityManager.verify_token(session)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )

    # Check session in database
    user_session = SecurityManager.get_session(db, session)
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found or expired"
        )

    # Get user
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


def require_admin(user: User = None) -> User:
    """
    Dependency to require admin role.

    Args:
        user: Current user (from get_current_user dependency)

    Returns:
        User: Admin user

    Raises:
        HTTPException: If user is not an admin
    """
    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


def set_session_cookie(response: Response, token: str) -> None:
    """
    Set session cookie in response.

    Args:
        response: FastAPI response object
        token: Session token to set
    """
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=True,  # Set to False for local development without HTTPS
        samesite="strict",
        max_age=settings.JWT_EXPIRATION_HOURS * 3600
    )


def clear_session_cookie(response: Response) -> None:
    """
    Clear session cookie from response.

    Args:
        response: FastAPI response object
    """
    response.delete_cookie(key="session", httponly=True, secure=True, samesite="strict")

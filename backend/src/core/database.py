"""
Database Configuration and Session Management
SQLAlchemy setup for PostgreSQL with multi-schema support
"""

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

from src.core.config import settings

logger = logging.getLogger(__name__)

# ============================================================================
# Database Engine
# ============================================================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using
    pool_size=10,  # Connection pool size
    max_overflow=20,  # Max overflow connections
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# ============================================================================
# Session Factory
# ============================================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================================================
# Base Model with Multi-Schema Support
# ============================================================================

# Metadata for each schema
metadata_shared = MetaData(schema="shared")
metadata_meal_planning = MetaData(schema="meal_planning")

# Base classes for each schema
BaseShared = declarative_base(metadata=metadata_shared)
BaseMealPlanning = declarative_base(metadata=metadata_meal_planning)

# Generic Base (will be used as reference)
Base = declarative_base()

# ============================================================================
# Dependency Injection
# ============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI endpoints.

    Usage:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db session
            pass

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# Database Utilities
# ============================================================================

def init_db() -> None:
    """Initialize database (create tables if they don't exist)"""
    logger.info("Initializing database")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")

def check_db_connection() -> bool:
    """
    Check if database connection is working.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

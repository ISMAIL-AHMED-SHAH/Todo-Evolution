"""
Database connection setup for Neon PostgreSQL with SQLModel

Features:
- Connection pooling for optimal performance
- Automatic connection health checks (pool_pre_ping)
- Connection recycling to prevent stale connections
- Error handling and rollback support
- Development/production environment support
"""
from sqlmodel import create_engine, Session
from typing import Generator
import os
from contextlib import contextmanager
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
# Look for .env in backend directory (three levels up from this file)
# Priority: backend/.env > project_root/.env
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Setup logging
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# For development: Use non-pooled endpoint to avoid stale schema cache
# Neon's pooler can cache schema, causing issues after migrations
# For development: Use non-pooled endpoint to avoid stale schema cache
if "neon.tech" in DATABASE_URL and "-pooler" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("-pooler", "")
    print("[DATABASE] Switched to non-pooled Neon endpoint to avoid schema cache issues")

# Environment-specific settings
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"

# Create engine with appropriate settings for Neon
try:
    from sqlmodel import SQLModel

    # Import models FIRST to register them with SQLModel.metadata
    # This ensures we use model definitions, not database reflection
    from src.models.user import User
    from src.models.task import Task

    # Create engine with Neon-optimized settings
    # IMPORTANT: Engine is created AFTER models are imported
    # This ensures SQLAlchemy uses our model definitions as source of truth
    engine = create_engine(
        DATABASE_URL,
        # Connection pooling settings for Neon Serverless PostgreSQL
        pool_size=5,              # Number of connections to keep open
        max_overflow=10,          # Additional connections allowed when pool is full
        pool_pre_ping=True,       # Verify connections before use (auto-reconnect)
        pool_recycle=300,         # Recycle connections after 5 minutes
        pool_reset_on_return='rollback',  # Reset connection state on return to pool
        echo=not IS_PRODUCTION,   # Log SQL queries in development
        # Timeout settings
        connect_args={
            "connect_timeout": 10,  # Connection timeout in seconds
        }
    )

    logger.info("Database engine created successfully")
    logger.info(f"Database URL: {DATABASE_URL[:50]}...")  # Log truncated URL
    logger.info(f"Registered models: {list(SQLModel.metadata.tables.keys())}")

    # Verify the User model has password_hash in metadata
    if 'user' in SQLModel.metadata.tables:
        user_columns = [col.name for col in SQLModel.metadata.tables['user'].columns]
        logger.info(f"User table columns in metadata: {user_columns}")
        if 'password_hash' not in user_columns:
            logger.error("CRITICAL: password_hash column missing from User metadata!")
    else:
        logger.error("CRITICAL: 'user' table not found in SQLModel metadata!")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise


def get_session() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection

    Provides a database session with automatic cleanup and error handling.
    Used as a FastAPI dependency for endpoint handlers.

    Yields:
        Session: SQLModel database session

    Raises:
        Exception: If database connection or operation fails
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise


@contextmanager
def get_db_session():
    """
    Context manager for database sessions

    Provides a database session with automatic transaction management.
    Commits on success, rolls back on error.

    Yields:
        Session: SQLModel database session

    Example:
        with get_db_session() as session:
            user = User(email="test@example.com")
            session.add(user)
            # Automatically commits if no exception
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
        logger.debug("Database transaction committed")
    except Exception as e:
        session.rollback()
        logger.error(f"Database transaction rolled back: {e}")
        raise
    finally:
        session.close()
        logger.debug("Database session closed")


def init_db():
    """
    Initialize the database by creating all tables

    Creates all database tables defined in SQLModel models.
    Safe to call multiple times - only creates missing tables.

    Note:
        For production, use Alembic migrations instead of this function.
        This function is primarily for development and testing.

    Raises:
        Exception: If table creation fails
    """
    try:
        from src.models.user import User
        from src.models.task import Task
        from sqlmodel import SQLModel

        # Create all tables
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {e}")
        raise


def check_db_connection():
    """
    Check if database connection is healthy

    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        with Session(engine) as session:
            # Execute a simple query to test connection
            session.exec("SELECT 1")
        logger.info("Database connection check: OK")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
"""
Database configuration and initialization for DayPilot application.

Provides SQLAlchemy setup with SQLite backend and async support.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import structlog

from app.core.config import get_settings

logger = structlog.get_logger()
settings = get_settings()

# Create async engine for SQLite
# Note: SQLite with aiosqlite for async support
DATABASE_URL = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create declarative base for models
Base = declarative_base()
metadata = MetaData()


async def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    This is called during application startup.
    """
    try:
        async with engine.begin() as conn:
            # Import all models here to ensure they're registered
            from app.models import task, schedule, user_context, ml_models
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database sessions.
    
    Usage:
        async with get_db_session() as session:
            # Use session for database operations
            pass
    """
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI endpoints to get database session.
    
    Usage in FastAPI endpoints:
        async def endpoint(db: AsyncSession = Depends(get_db)):
            # Use db session
            pass
    """
    async with get_db_session() as session:
        yield session
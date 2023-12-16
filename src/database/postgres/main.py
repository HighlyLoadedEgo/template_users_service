from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.database.postgres.config import DatabaseConfig


def get_engine(config: DatabaseConfig, async_: bool = True) -> AsyncEngine:
    """Create an engine for the database."""
    engine = create_async_engine(config.db_url(async_=async_))

    return engine


def session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create a session for the database."""
    return async_sessionmaker(engine, autocommit=False, autoflush=False)


async def create_sa_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """
    Получение сессии для работы с бд
    """
    async with session_factory() as session:
        yield session

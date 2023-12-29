from typing import (
    AsyncGenerator,
    Generator,
)

from sqlalchemy import (
    Engine,
    create_engine,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

from src.core.database.postgres.config import DatabaseConfig


def get_engine(config: DatabaseConfig, async_: bool = True) -> AsyncEngine | Engine:
    """Create an engine for the database."""
    if async_:
        return create_async_engine(config.db_url(async_=async_))
    else:
        return create_engine(config.db_url(async_=async_))


def sync_session_maker(sync_engine: Engine) -> sessionmaker[Session]:
    """Create a sync session for the database."""
    return sessionmaker(sync_engine, autocommit=False, autoflush=False)


def async_session_maker(async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create an async session for the database."""
    return async_sessionmaker(async_engine, autocommit=False, autoflush=False)


async def create_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """
    Получение асинхронной сессии для работы с бд
    """
    async with session_factory() as session:
        yield session


def create_sync_session(
    session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    """
    Получение синхронной сессии для работы с бд
    """
    with session_factory() as session:
        yield session

from typing import (
    AsyncGenerator,
    Generator,
)

import pytest
import pytest_asyncio
from alembic.command import (
    downgrade,
    upgrade,
)
from alembic.config import Config as AlembicConfig
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)
from testcontainers.postgres import PostgresContainer  # type: ignore

from src.application.api.config import (
    AppConfig,
    Settings,
)
from src.application.di.di_builder import build_di
from src.application.main import init_app
from src.application.routers_init import init_routers
from src.core.utils.config_loader import load_config
from tests.integrinity.factories import postgres as postgres_factories
from tests.integrinity.factories.postgres.base import BaseFactory

for pg_factory in postgres_factories.__registry_factories__:
    register(pg_factory)


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer() as postgres:
        yield postgres


@pytest.fixture(scope="session")
def postgres_url(postgres_container: PostgresContainer) -> str:
    return postgres_container.get_connection_url()


@pytest.fixture(scope="session")
def postgres_async_url(postgres_container: PostgresContainer) -> str:
    return postgres_container.get_connection_url().replace("psycopg2", "asyncpg")


@pytest.fixture
def alembic_config(postgres_url: str) -> AlembicConfig:
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_cfg


@pytest.fixture
def init_db_tables(alembic_config: AlembicConfig) -> Generator[None, None, None]:
    upgrade(alembic_config, "head")
    yield
    downgrade(alembic_config, "base")


@pytest.fixture
def sync_session_factory(
    postgres_url: str,
) -> Generator[sessionmaker[Session], None, None]:
    sync_engine = create_engine(postgres_url)
    session_factory_: sessionmaker[Session] = sessionmaker(
        sync_engine, autocommit=False, autoflush=False, expire_on_commit=False
    )
    yield session_factory_
    sync_engine.dispose()


@pytest_asyncio.fixture
async def async_session_factory(
    postgres_async_url: str,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    async_engine = create_async_engine(url=postgres_async_url)
    session_factory_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        async_engine, autocommit=False, autoflush=False, expire_on_commit=False
    )
    yield session_factory_
    await async_engine.dispose()


@pytest.fixture
def sync_session(
    init_db_tables: None,
    sync_session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    with sync_session_factory() as sync_session:
        yield sync_session


@pytest_asyncio.fixture
async def async_session(
    init_db_tables: None,
    async_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as async_session:
        yield async_session


@pytest.fixture(autouse=True)
def set_factory_session(sync_session: Session) -> None:
    BaseFactory.set_session(sync_session)


@pytest.fixture
def get_test_settings(postgres_async_url: str, postgres_url: str) -> Settings:
    class DatabaseTestConfig:
        @staticmethod
        def db_url(async_: bool) -> str:
            return postgres_async_url if async_ else postgres_url

    settings = load_config(Settings)
    settings.database = DatabaseTestConfig()  # type: ignore

    return settings


@pytest.fixture
def test_fastapi_app(get_test_settings: Settings) -> FastAPI:
    app = init_app(load_config(AppConfig, config_scope="app"))
    build_di(config=get_test_settings, app=app)
    init_routers(app=app)
    return app


@pytest.fixture
def client(init_db_tables: None, test_fastapi_app: FastAPI) -> TestClient:
    return TestClient(test_fastapi_app)

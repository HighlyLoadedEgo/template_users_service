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
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

# from src.application.di.providers.users.stubs import user_uow_stub
from src.application.endpoints_init import init_endpoints

# from src.application.api.config import Settings


# from src.core.auth.stubs import jwt_manager_stub
# from src.core.utils.config_loader import load_config

# from src.modules.users.stubs import get_service_stub


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer(port=5454) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def postgres_url(postgres_container: PostgresContainer) -> str:
    return postgres_container.get_connection_url()


@pytest.fixture(scope="session")
def postgres_async_url(postgres_container: PostgresContainer) -> str:
    return postgres_container.get_connection_url().replace("psycopg2", "asyncpg")


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> AlembicConfig:
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_cfg


@pytest.fixture
def init_db_tables(alembic_config: AlembicConfig) -> Generator[None, None, None]:
    upgrade(alembic_config, "head")
    yield
    downgrade(alembic_config, "base")


@pytest_asyncio.fixture(scope="session")
async def session_factory(
    postgres_async_url: str,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    async_engine = create_async_engine(url=postgres_async_url)
    session_factory_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        engine=async_engine, autocommit=False, autoflush=False, expire_on_commit=False
    )
    yield session_factory_
    await async_engine.dispose()


@pytest_asyncio.fixture
async def async_session():
    pass


@pytest.fixture(scope="session")
def test_fastapi_app() -> FastAPI:
    app = FastAPI()
    init_endpoints(app=app)
    # application_config = load_config(Settings)

    # app.dependency_overrides[get_service_stub] = get_user_service
    # app.dependency_overrides[user_uow_stub] = user_uow_provider.user_uow
    # app.dependency_overrides[jwt_manager_stub] = lambda: jwt_manager
    return app


@pytest.fixture(scope="session")
def client(test_fastapi_app: FastAPI) -> TestClient:
    return TestClient(test_fastapi_app)

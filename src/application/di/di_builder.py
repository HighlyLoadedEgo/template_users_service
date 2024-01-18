from fastapi import FastAPI

from src.application.api.config import Settings
from src.application.di.providers.users.service import get_user_service
from src.application.di.providers.users.stubs import (
    get_service_stub,
    user_uow_stub,
)
from src.application.di.providers.users.uow import UserUoWProvider
from src.core.auth.jwt import JWTManagerImpl
from src.core.auth.stubs import jwt_manager_stub
from src.core.database.postgres.main import (
    async_session_maker,
    get_engine,
)


def build_di(app: FastAPI, config: Settings) -> None:
    """Create an instance and override the depends."""
    async_engine = get_engine(config=config.database, async_=True)
    user_uow_provider = UserUoWProvider(
        session_maker=async_session_maker(async_engine=async_engine)  # type: ignore
    )
    jwt_manager = JWTManagerImpl(jwt_config=config.jwt)

    app.dependency_overrides = {
        get_service_stub: get_user_service,
        user_uow_stub: user_uow_provider.user_uow,
        jwt_manager_stub: lambda: jwt_manager,
    }

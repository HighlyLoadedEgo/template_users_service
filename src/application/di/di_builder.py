from fastapi import FastAPI

from src.application.api.config import Settings
from src.application.di.providers.users.service import get_user_service
from src.application.di.providers.users.stubs import user_uow_stub
from src.application.di.providers.users.uow import UserUoWProvider
from src.core.auth.jwt import JWTManagerImpl
from src.core.auth.stubs import jwt_manager_stub
from src.core.database.postgres.main import (
    async_session_maker,
    get_engine,
)
from src.modules.users.stubs import get_service_stub


def build_di(app: FastAPI, config: Settings) -> None:
    async_engine = get_engine(config=config.database, async_=True)
    user_uow_provider = UserUoWProvider(
        session_maker=async_session_maker(async_engine=async_engine)  # type: ignore
    )
    jwt_manager = JWTManagerImpl(config=config.jwt)

    app.dependency_overrides[get_service_stub] = get_user_service
    app.dependency_overrides[user_uow_stub] = user_uow_provider.user_uow
    app.dependency_overrides[jwt_manager_stub] = lambda: jwt_manager

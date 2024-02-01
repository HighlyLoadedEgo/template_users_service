from fastapi import FastAPI
from faststream.rabbit import RabbitBroker

from src.application.config import Settings
from src.application.di.providers.users.message_sender import MessageSenderProvider
from src.application.di.providers.users.service import get_user_service
from src.application.di.providers.users.stubs import (
    get_service_stub,
    msg_broker_stub,
    user_uow_stub,
)
from src.application.di.providers.users.uow import UserUoWProvider
from src.core.auth.jwt import JWTManagerImpl
from src.core.auth.stubs import jwt_manager_stub


def build_di(app: FastAPI, config: Settings, broker: RabbitBroker) -> None:
    """Create an instance and override the depends."""
    user_uow_provider = UserUoWProvider(config=config.database)
    jwt_manager = JWTManagerImpl(jwt_config=config.jwt)
    msg_broker = MessageSenderProvider(msg_broker=broker)

    app.dependency_overrides = {
        get_service_stub: get_user_service,
        user_uow_stub: user_uow_provider.user_uow,
        jwt_manager_stub: lambda: jwt_manager,
        msg_broker_stub: msg_broker.msg_sender,
    }

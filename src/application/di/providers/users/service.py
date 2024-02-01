from fastapi import Depends

from src.application.di.providers.users.stubs import (
    msg_broker_stub,
    user_uow_stub,
)
from src.core.auth.common.jwt import JWTManager
from src.core.auth.stubs import jwt_manager_stub
from src.core.message_queue.common.broker import MessageSender
from src.modules.users import UserService
from src.modules.users.uow import UserUoW


def get_user_service(
    uow: UserUoW = Depends(user_uow_stub),
    jwt_manager: JWTManager = Depends(jwt_manager_stub),
    msg_broker: MessageSender = Depends(msg_broker_stub),
) -> UserService:
    """Return instance of the user service."""

    return UserService(uow=uow, jwt_manager=jwt_manager, msg_broker=msg_broker)

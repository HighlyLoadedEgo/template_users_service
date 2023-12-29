from fastapi import Depends

from src.application.di.providers.users.stubs import user_uow_stub
from src.modules.users import UserService
from src.modules.users.uow import UserUoW


def get_user_service(uow: UserUoW = Depends(user_uow_stub)) -> UserService:
    return UserService(uow=uow)

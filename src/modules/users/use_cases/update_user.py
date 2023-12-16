from src.common.interfaces.use_case import UseCase
from src.modules.users.schemas import UpdateUserSchema
from src.modules.users.uow import UserUoW


class UpdateUserUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, update_user_data: UpdateUserSchema) -> None:
        """Update user."""
        async with self._uow as uow:
            await uow.user_repository.update_user(update_user_data=update_user_data)

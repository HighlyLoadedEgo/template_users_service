from uuid import UUID

from src.common.interfaces.use_case import UseCase
from src.modules.users.uow import UserUoW


class DeleteUserUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, user_id: UUID) -> None:
        """Delete user."""
        async with self._uow as uow:
            await uow.user_repository.delete_user(user_id=user_id)

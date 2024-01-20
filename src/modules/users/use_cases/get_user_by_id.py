from uuid import UUID

from src.core.common.interfaces.use_case import UseCase
from src.modules.users.dtos import FullUserSchema
from src.modules.users.exceptions import UserDoesNotExistException
from src.modules.users.uow import UserUoW


class GetUserByIdUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, user_id: UUID) -> FullUserSchema:
        """Get a user by id."""
        user: FullUserSchema | None = await self._uow.user_repository.get_user_by_id(
            user_id=user_id
        )

        if not user:
            raise UserDoesNotExistException(search_data=user_id)

        return user

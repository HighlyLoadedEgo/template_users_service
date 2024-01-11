from uuid import UUID

from src.core.common.interfaces.use_case import UseCase
from src.modules.users.schemas import FullUserSchema
from src.modules.users.uow import UserUoW


class GetUserByIdUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, user_id: UUID) -> FullUserSchema | None:
        """Get a user by id."""
        user = await self._uow.user_repository.get_user_by_id(user_id=user_id)

        full_user_data = FullUserSchema.model_validate(user)

        return full_user_data

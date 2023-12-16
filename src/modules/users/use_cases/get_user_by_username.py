from src.common.interfaces.use_case import UseCase
from src.modules.users.schemas import FullUserSchema
from src.modules.users.uow import UserUoW


class GetUserByUsernameUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, username: str) -> FullUserSchema:
        """Get a user by username."""
        user = await self._uow.user_reader.get_user_by_username(username=username)

        full_user_data = FullUserSchema.model_validate(user)

        return full_user_data

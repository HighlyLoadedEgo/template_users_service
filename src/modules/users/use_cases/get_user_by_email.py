from src.common.interfaces.use_case import UseCase
from src.modules.users.schemas import FullUserSchema
from src.modules.users.uow import UserUoW


class GetUserByEmailUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, email: str) -> FullUserSchema:
        """Get a user by email."""
        updated_user = await self._uow.user_reader.get_user_by_email(email=email)

        full_user_data = FullUserSchema.model_validate(updated_user)

        return full_user_data

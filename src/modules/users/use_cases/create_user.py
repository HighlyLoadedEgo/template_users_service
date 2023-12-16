from src.common.interfaces.use_case import UseCase
from src.modules.users.schemas import (
    CreateUserSchema,
    FullUserSchema,
)
from src.modules.users.uow import UserUoW


class CreateUserUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, create_user_data: CreateUserSchema) -> FullUserSchema:
        """Create user."""
        async with self._uow as uow:
            created_user = await uow.user_repository.create_user(
                create_user_data=create_user_data
            )

        full_user_data = FullUserSchema.model_validate(created_user)

        return full_user_data

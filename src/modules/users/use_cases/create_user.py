from src.core.common.interfaces.use_case import UseCase
from src.modules.users.dtos import CreateUserSchema
from src.modules.users.uow import UserUoW
from src.modules.users.utils import generate_password_hash


class CreateUserUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, create_user_data: CreateUserSchema) -> None:
        """Create user."""
        create_user_data.password = generate_password_hash(create_user_data.password)

        await self._uow.user_repository.create_user(create_user_data=create_user_data)

        await self._uow.commit()

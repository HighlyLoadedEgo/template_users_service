from src.core.common.interfaces.use_case import UseCase
from src.modules.users.exceptions import IncorrectUserCredentialsException
from src.modules.users.schemas import (
    FullUserSchema,
    LoginUserSchema,
)
from src.modules.users.uow import UserUoW
from src.modules.users.utils import verify_password_hash


class CheckValidUserUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, user_credentials: LoginUserSchema) -> FullUserSchema:
        """Get a user by id."""
        user = await self._uow.user_reader.get_user_by_username(
            username=user_credentials.username
        )
        full_user_data = FullUserSchema.model_validate(user)

        password_verified = verify_password_hash(
            password=user_credentials.password,
            hashed_password=full_user_data.hashed_password,
        )

        if password_verified:
            return full_user_data

        raise IncorrectUserCredentialsException()

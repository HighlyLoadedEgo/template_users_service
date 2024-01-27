import structlog

from src.core.common.interfaces.use_case import UseCase
from src.modules.users.dtos import UpdateUserSchema
from src.modules.users.exceptions import UserDoesNotExistException
from src.modules.users.uow import UserUoW

logger = structlog.stdlib.get_logger(__name__)


class UpdateUserUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, update_user_data: UpdateUserSchema) -> None:
        """Update user."""
        user = await self._uow.user_repository.get_user_by_id(update_user_data.user_id)

        if not user:
            raise UserDoesNotExistException(search_data=update_user_data.user_id)

        await self._uow.user_repository.update_user(update_user_data=update_user_data)

        await self._uow.commit()

        logger.info(
            "User was successfully updated", user=user, update_data=update_user_data
        )

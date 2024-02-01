from uuid import UUID

import structlog

from src.core.common.interfaces.use_case import UseCase
from src.modules.users.dtos import FullUserSchema
from src.modules.users.exceptions import UserDoesNotExistException
from src.modules.users.uow import UserUoW

logger = structlog.stdlib.get_logger(__name__)


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

        logger.debug("Get user by id", user=user)

        return user

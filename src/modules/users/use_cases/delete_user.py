from uuid import UUID

import structlog

from src.core.common.interfaces.use_case import UseCase
from src.modules.users.uow import UserUoW

logger = structlog.stdlib.get_logger(__name__)


class DeleteUserUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(self, user_id: UUID) -> None:
        """Delete user."""
        await self._uow.user_repository.delete_user(user_id=user_id)

        await self._uow.commit()

        logger.info("User was deleted", user_id=user_id)

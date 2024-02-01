from uuid import UUID

import structlog

from src.core.common.interfaces.use_case import UseCase
from src.core.message_queue.common.broker import MessageSender
from src.core.message_queue.constants import MessageRoutingKey
from src.modules.users.dtos import BrokerMessageSchema
from src.modules.users.uow import UserUoW

logger = structlog.stdlib.get_logger(__name__)


class DeleteUserUseCase(UseCase):
    def __init__(self, uow: UserUoW, msg_broker: MessageSender):
        self._uow = uow
        self._msg_broker = msg_broker

    async def __call__(self, user_id: UUID) -> None:
        """Delete user."""
        deleted_user = await self._uow.user_repository.delete_user(user_id=user_id)

        await self._uow.commit()

        logger.info("User was deleted", user_id=user_id)

        if deleted_user:
            await self._msg_broker.message(
                routing_key=MessageRoutingKey.MAILING_DELETE,
                message=BrokerMessageSchema(user_email=deleted_user.email),  # type: ignore
            )

            logger.info(
                "Message successfully sent",
                user_email=deleted_user.email,
            )

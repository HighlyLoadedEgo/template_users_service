import structlog

from src.core.common.interfaces.use_case import UseCase
from src.core.message_queue.common.broker import MessageSender
from src.core.message_queue.constants import MessageRoutingKey
from src.modules.users.dtos import (
    BrokerMessageSchema,
    UpdateUserSchema,
)
from src.modules.users.exceptions import UserDoesNotExistException
from src.modules.users.uow import UserUoW

logger = structlog.stdlib.get_logger(__name__)


class UpdateUserUseCase(UseCase):
    def __init__(self, uow: UserUoW, msg_broker: MessageSender):
        self._uow = uow
        self._msg_broker = msg_broker

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

        await self._msg_broker.message(
            routing_key=MessageRoutingKey.MAILING_UPDATE,
            message=BrokerMessageSchema(user_email=user.email),  # type: ignore
        )

        logger.info(
            "Message successfully sent",
            user_email=user.email,
        )

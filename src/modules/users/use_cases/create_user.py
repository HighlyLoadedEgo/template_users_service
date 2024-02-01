import structlog

from src.core.common.interfaces.use_case import UseCase
from src.core.message_queue.common.broker import MessageSender
from src.core.message_queue.constants import MessageRoutingKey
from src.modules.users.dtos import (
    BrokerMessageSchema,
    CreateUserSchema,
)
from src.modules.users.uow import UserUoW
from src.modules.users.utils import generate_password_hash

logger = structlog.stdlib.get_logger(__name__)


class CreateUserUseCase(UseCase):
    def __init__(self, uow: UserUoW, msg_broker: MessageSender):
        self._uow = uow
        self._msg_broker = msg_broker

    async def __call__(self, create_user_data: CreateUserSchema) -> None:
        """Create user."""
        create_user_data.password = generate_password_hash(create_user_data.password)

        await self._uow.user_repository.create_user(create_user_data=create_user_data)

        await self._uow.commit()

        logger.info(
            "User created successfully",
            user=create_user_data.model_dump(exclude={"password"}),
        )

        await self._msg_broker.message(
            routing_key=MessageRoutingKey.MAILING_WELCOME,
            message=BrokerMessageSchema(user_email=create_user_data.email),  # type: ignore
        )

        logger.info(
            "Message successfully sent",
            user_email=create_user_data.email,
        )

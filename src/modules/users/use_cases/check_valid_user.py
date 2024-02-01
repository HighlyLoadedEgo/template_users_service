import structlog

from src.core.auth import (
    TokensData,
    UserPayload,
)
from src.core.auth.common.jwt import JWTManager
from src.core.common.interfaces.use_case import UseCase
from src.core.message_queue.common.broker import MessageSender
from src.core.message_queue.constants import MessageRoutingKey
from src.modules.users.dtos import (
    BrokerMessageSchema,
    LoginUserSchema,
)
from src.modules.users.exceptions import IncorrectUserCredentialsException
from src.modules.users.uow import UserUoW
from src.modules.users.utils import verify_password_hash

logger = structlog.stdlib.get_logger(__name__)


class CheckValidUserUseCase(UseCase):
    def __init__(
        self, uow: UserUoW, jwt_manager: JWTManager, msg_broker: MessageSender
    ):
        self._uow = uow
        self._jwt_manager = jwt_manager
        self._msg_broker = msg_broker

    async def __call__(self, user_credentials: LoginUserSchema) -> TokensData:
        """Get a user by id."""
        user = await self._uow.user_reader.get_user_by_username(
            username=user_credentials.username
        )

        if not user:
            raise IncorrectUserCredentialsException()

        password_verified = verify_password_hash(
            password=user_credentials.password,
            hashed_password=user.hashed_password,
        )

        if not password_verified:
            raise IncorrectUserCredentialsException()

        token_data = self._jwt_manager.encode_token(
            payload=UserPayload.model_validate(user)
        )

        logger.info("User verified", username=user.username)

        await self._msg_broker.message(
            routing_key=MessageRoutingKey.MAILING_LOGIN,
            message=BrokerMessageSchema(user_email=user.email),  # type: ignore
        )

        logger.info(
            "Message successfully sent",
            user_email=user.email,
        )

        return token_data

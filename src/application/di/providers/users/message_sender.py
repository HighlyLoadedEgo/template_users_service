from typing import AsyncGenerator

import structlog
from faststream.rabbit import RabbitBroker

from src.core.message_queue.broker import MessageSenderImpl
from src.core.message_queue.main import get_msg_broker

logger = structlog.stdlib.get_logger(__name__)


class MessageSenderProvider:
    __message_sender: None | MessageSenderImpl = None

    def __init__(self, msg_broker: RabbitBroker) -> None:
        self._msg_broker = msg_broker

    async def msg_sender(self) -> AsyncGenerator[MessageSenderImpl, None]:
        if self.__message_sender is None:
            self.__message_sender = await get_msg_broker(self._msg_broker)
        yield self.__message_sender

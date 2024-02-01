from faststream.rabbit import (
    RabbitBroker,
    RabbitExchange,
)
from pydantic import BaseModel

from src.core.message_queue.common.broker import MessageSender
from src.core.message_queue.constants import MessageRoutingKey


class MessageSenderImpl(MessageSender):
    def __init__(
        self,
        msg_broker: RabbitBroker,
        exchanges: dict[MessageRoutingKey, RabbitExchange],
    ) -> None:
        self._broker = msg_broker
        self._exchanges = exchanges

    async def message(self, routing_key: MessageRoutingKey, message: BaseModel) -> None:
        """Method to send a message to the queue by exchanges."""
        exchange = self._exchanges.get(routing_key)
        await self._broker.publish(
            message=message, routing_key=routing_key.value, exchange=exchange
        )

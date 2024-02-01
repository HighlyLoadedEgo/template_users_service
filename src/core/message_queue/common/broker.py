from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel

from src.core.message_queue.constants import MessageRoutingKey


class MessageSender(ABC):
    @abstractmethod
    async def message(self, routing_key: MessageRoutingKey, message: BaseModel) -> None:
        """Method to send a message to the queue."""

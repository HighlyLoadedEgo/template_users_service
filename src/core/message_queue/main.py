from faststream.rabbit import RabbitBroker

from src.core.message_queue.broker import MessageSenderImpl
from src.core.message_queue.exchanges import get_exchanges_mapper


async def get_msg_broker(msg_broker: RabbitBroker) -> MessageSenderImpl:
    """Initialize a MessageBroker."""
    exchanges_mapper = await get_exchanges_mapper(msg_broker)
    message_sender = MessageSenderImpl(
        msg_broker=msg_broker, exchanges=exchanges_mapper
    )

    return message_sender

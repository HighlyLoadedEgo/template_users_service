from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
)

from src.core.message_queue.constants import (
    MessageExchanges,
    MessageRoutingKey,
)


async def get_exchanges_mapper(
    broker: RabbitBroker,
) -> dict[MessageRoutingKey, RabbitExchange]:
    mailing_topic = RabbitExchange(
        name=MessageExchanges.USERS_MAILING.value, type=ExchangeType.TOPIC
    )

    await broker.declare_exchange(mailing_topic)

    exchanges_mapper = {
        MessageRoutingKey.MAILING_WELCOME: mailing_topic,
        MessageRoutingKey.MAILING_LOGIN: mailing_topic,
        MessageRoutingKey.MAILING_UPDATE: mailing_topic,
        MessageRoutingKey.MAILING_DELETE: mailing_topic,
    }
    return exchanges_mapper

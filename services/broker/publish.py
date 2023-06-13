import asyncio
import logging

from aio_pika import Message, DeliveryMode

from services.common.utils import serialize_dict
from services.broker.base_class import MessageBroker
from services.broker import exceptions
from services.broker.schemas import OrderMQSchema


logger = logging.getLogger("collections_core_log")


async def publish_message(broker: MessageBroker, order: OrderMQSchema):
    channel = None
    try:
        if not broker:
            raise exceptions.BrokerNotSet

        # нужно локать event-loop, т.к. у нас 1 глобальный объект брокера
        async with asyncio.Lock():
            await broker.check_connection_state()
            channel = await broker.create_channel()
            queue_name = broker.queue_name
        payload = serialize_dict(order.dict())
        await channel.default_exchange.publish(
            message=Message(body=payload, content_type="application/json", delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=queue_name,
        )
        logger.info(f"Message sent: {payload}")
    except Exception as e:
        raise exceptions.MessagePublishException(detail=str(e))
    finally:
        if channel and not channel.is_closed:
            await channel.close()

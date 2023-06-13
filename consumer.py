import json
import asyncio
import aio_pika
import logging
from typing import Optional

import pydantic

from services.match_engine.engine import receiveOrder
from services.db.db import Session
from services.broker.schemas import OrderMQSchema

from config.config import settings


logger = logging.getLogger("consumer")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s - %(asctime)s]: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def validate_message(
        message: aio_pika.IncomingMessage
) -> Optional[OrderMQSchema]:
    """Валидирует входящее сообщения от брокера, используя pydantic

    :param message: объект сообщения от брокера
    :type message: aio_pika.message.IncomingMessage
    :return: словарь с телом сообщения
    :rtype: None or EventBase
    """
    try:
        message_body = json.loads(message.body.decode())
        logger.info(f"Got new message: {message_body}")
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Incoming message is invalid: {e}")
        return None
    try:
        if isinstance(message_body, dict):
            order = OrderMQSchema(**message_body)
        else:
            logger.error("Incoming message is invalid")
            return None
    except (pydantic.ValidationError, KeyError) as e:
        logger.error(f"Incoming message is invalid: {e}")
        return None
    else:
        logger.info("Incoming message is valid")
        return order


async def main(loop):
    connection = await aio_pika.connect_robust(
        settings.RABBITMQ_URL, loop=loop
    )

    queue_name = settings.RABBITMQ_QUEUE_NAME

    logger.info("Consumer startup complete")

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                order = validate_message(message=message)
                if order is None:
                    await message.ack()
                else:
                    async with Session() as session:
                        consume_result = await receiveOrder(db=session, order=order)
                    if consume_result:
                        await message.ack()
                    else:
                        await message.nack()
                        break  # stop consumer


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main(event_loop))
    event_loop.close()

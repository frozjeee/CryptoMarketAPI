import asyncio
from jose import JWTError, jwt
from configs.config import (
    SECRET_KEY,
    ALGORITHM,
    credentialsException,
    unauthorizedException
)
from schemas import TokenData

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.patterns import RPC
from configs.kafkaConfig import loop


async def validateToken():
    connection = await connect_robust(
        "amqp://admin:admin@localhost:5672/",
        client_properties={"connection_name": "callee"},
    )

    # Creating channel
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    await rpc.register("validate-token", min, auto_delete=True)

    try:
        await asyncio.Future()
    finally:
        await connection.close()

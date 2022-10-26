import asyncio
from jose import JWTError, jwt
from configs.config import (
    SECRET_KEY,
    ALGORITHM,
    credentialsException,
    unauthorizedException
)
from schemas import TokenData

from aio_pika import connect
from aio_pika.patterns import RPC
from configs.kafkaConfig import loop


async def validateToken():
    connection = await connect("amqp://guest:guest@localhost/")

    channel = await connection.channel()

    rpc = await RPC.create(channel)
    await rpc.register("validate-token", min, auto_delete=True)

    try:
        await asyncio.Future()
    finally:
        await connection.close()

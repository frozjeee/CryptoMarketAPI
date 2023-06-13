import asyncio
import logging

from aio_pika import RobustConnection
from aio_pika.connection import make_url
from aio_pika.abc import AbstractChannel

from config.config import settings


logger = logging.getLogger("market_rmq")


class MessageBroker:
    """Класс для интеграции с RabbitMQ.

    Класс отвечает за:
        1) TCP подключение к RabbitMQ
        2) менеджерит lifecycle объектов Channel

    При потере TCP подключения (если rabbitmq отвалился) пытается
    сделать реконнект каждые RABBITMQ_RECONNECT_INTERVAL

    Проверка подключения происходит перед каждой попыткой отправки сообщения
    """
    def __init__(
            self,
            connection_url: str = settings.RABBITMQ_URL,
            queue_name: str = settings.RABBITMQ_QUEUE_NAME,
            loop: asyncio.AbstractEventLoop = None
    ):
        self.connection_url = connection_url
        self.queue_name = queue_name
        self.loop = loop or asyncio.get_event_loop()
        self.connection = RobustConnection(
            url=make_url(self.connection_url),
            loop=self.loop
        )
        self.connection.reconnect_interval = settings.RABBITMQ_RECONNECT_INTERVAL

    async def startup(self):
        try:
            # fail_fast отвечает за reconnect
            # если True, будет возвращена ошибка подключения
            # сразу после 1-й попытки
            self.connection.fail_fast = False
            await self.connection.connect()
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}")

    async def shutdown(self):
        if not self.connection.is_closed:
            await self.connection.close()

    async def check_connection_state(self):
        try:
            await asyncio.wait_for(self.connection.connected.wait(), timeout=1)
        except asyncio.TimeoutError:
            self.connection.connected.clear()
        if not self.connection.connected.is_set():
            raise Exception()

    async def create_channel(self) -> AbstractChannel:
        try:
            return await self.connection.channel()
        except ConnectionError:
            raise Exception()


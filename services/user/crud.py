from datetime import datetime
from aiokafka import AIOKafkaConsumer
from fastapi.security import OAuth2PasswordBearer
from schemas import UserId, UserIn, UserOut, UserUpdate
from db import User, database as db
from passlib.context import CryptContext
import configs.kafkaConfig as kafkaConfig


oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def getUserByEmail(email):
    query = User.select()
    return await db.fetch_one(query=query, values=email)


async def createUser(settings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(settings.REGISTER_TOPIC,
                                loop=settings.loop(),
                                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=settings.USER_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = UserIn.parse_raw(msg.value)
            payload.password = pwdContext.hash(payload.password)
            payload.updated_at = datetime.today().replace(microsecond=0)
            payload.created_at = datetime.today().replace(microsecond=0)
            query = User.insert().values(dict(payload))
            await db.execute(query=query)
    finally:
        await consumer.stop()


async def deleteUser(settings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(settings.USER_DELETE_TOPIC,
                                loop=settings.loop(),
                                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=settings.USER_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = UserOut.parse_raw(msg.value)
            query = User.delete().where(User.c.id==payload.id)
            await db.execute(query=query)
    finally:
        await consumer.stop()


async def updateUser(settings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(settings.USER_UPDATE_TOPIC,
                                loop=settings.loop(),
                                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=settings.USER_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = UserUpdate.parse_raw(msg.value)
            payload.updated_at = datetime.today().replace(microsecond=0)
            query = User.update().where(User.c.id==payload.id) \
                                .values(payload.dict(exclude_none=True))
            await db.execute(query=query)
    finally:
        await consumer.stop()


async def verifiedUser(settings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(settings.USER_VERIFIED_TOPIC,
                                loop=settings.loop(),
                                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=settings.USER_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = UserId.parse_raw(msg.value)
            query = User.update().where(User.c.id==payload.id) \
                                .values(verified=True)
            await db.execute(query=query)
    finally:
        await consumer.stop()

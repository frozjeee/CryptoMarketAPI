from aiokafka import AIOKafkaConsumer
from fastapi.security import OAuth2PasswordBearer
from schemas import UserIn, UserOut, UserUpdate
from db import User, database as db
from configs.kafkaConfig import (REGISTER_TOPIC, loop,
    KAFKA_BOOTSTRAP_SERVERS, USER_CONSUMER_GROUP, 
    USER_DELETE_TOPIC, USER_UPDATE_TOPIC)
from passlib.context import CryptContext
import json


oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def createUser():
    consumer = AIOKafkaConsumer(REGISTER_TOPIC,
                                loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=USER_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = UserIn.parse_raw(msg.value)
            payload.password = hashPassword(payload.password)
            query = User.insert().values(dict(payload))
            await db.execute(query=query)
    finally:
        await consumer.stop()


async def getUserByEmail(email):
    query = User.select()
    return await db.fetch_one(query=query, values=email)


async def deleteUser():
    consumer = AIOKafkaConsumer(USER_DELETE_TOPIC,
                                loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=USER_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = UserOut.parse_raw(msg.value)
            query = User.delete().where(User.c.id==payload.id)
            await db.execute(query=query)
    finally:
        await consumer.stop()


async def updateUser():
    consumer = AIOKafkaConsumer(USER_UPDATE_TOPIC,
                                loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=USER_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = UserUpdate.parse_raw(msg.value)
            query = User.update().where(User.c.id==payload.id) \
                                .values(payload.dict(exclude_none=True))
            await db.execute(query=query)
    finally:
        await consumer.stop()


def hashPassword(password):
    return pwdContext.hash(password)


def encodeToJson(payload):
    return json.dumps(json.loads(payload.json())).encode("utf-8")



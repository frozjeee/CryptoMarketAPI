from aiokafka import AIOKafkaConsumer
from db import database as db
from configs.kafkaConfig import (
    CURRENCY_CREATE_TOPIC, CURRENCY_UPDATE_TOPIC, CURRENCY_DELETE_TOPIC,
    KAFKA_BOOTSTRAP_SERVERS, CURRENCY_CONSUMER_GROUP, loop
    )
from schemas import CurrencyIn, CurrencyUpdate, CurrencyOut
from db import Currency
import json


async def createCurrency():
    consumer = AIOKafkaConsumer(CURRENCY_CREATE_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, 
                                group_id=CURRENCY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = CurrencyIn.parse_raw(msg.value)
            query = Currency.insert()
            return await db.execute(query=query, values=payload.dict())
    finally:
        await consumer.stop()
   

async def getCurrency(currencyName):
        query = Currency.select()
        return await db.fetch_one(query=query, 
                                  values={"currencyName": currencyName})


async def updateCurrency():
    consumer = AIOKafkaConsumer(CURRENCY_UPDATE_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, 
                                group_id=CURRENCY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = CurrencyUpdate.parse_raw(msg.value)
            query = Currency.update().where(Currency.c.id == payload.id) \
                                    .values(payload.dict(exclude_none=True))
            return await db.execute(query=query)
    finally:
        await consumer.stop()
    

async def deleteCurrency():
    consumer = AIOKafkaConsumer(CURRENCY_DELETE_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=CURRENCY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = CurrencyOut.parse_raw(msg.value)
            query = Currency.delete().where(Currency.c.id == payload.id)
            return await db.execute(query=query)
    finally:
        await consumer.stop()


def encodeToJson(payload):
    return json.dumps(json.loads(payload.json())).encode("utf-8")

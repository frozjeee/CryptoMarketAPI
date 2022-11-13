from uuid import uuid4

from aiokafka import AIOKafkaConsumer

from db import (
    Currency,
    MainCurrency,
    database as db
)

import configs.kafkaConfig as kafkaConfig
import schemas
    

async def createCurrency(
    payload: schemas.CurrencyIn,
    settings: kafkaConfig.Settings = kafkaConfig.getSettings()
):
    payload.id = uuid4()
    payload.market_cap = payload.quantity * payload.price
    query = Currency.insert()
    await db.execute(query=query, values=payload.dict())


async def createMainCurrency(
        settings: kafkaConfig.Settings = kafkaConfig.getSettings()
):

    consumer = AIOKafkaConsumer(
                settings.MAIN_CURRENCY_CREATE_TOPIC,
                loop=settings.loop(),
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=settings.CURRENCY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = MainCurrencyIn.parse_raw(msg.value)
            payload.id = uuid4()
            query = MainCurrency.insert()
            await db.execute(query=query, values=payload.dict())
    finally:
        await consumer.stop()


async def getCurrency(currencyName):
    query = Currency.select()
    return await db.fetch_one(
        query=query,
        values={"currencyName": currencyName}
    )


async def updateCurrency(
        settings: kafkaConfig.Settings = kafkaConfig.getSettings()
):

    consumer = AIOKafkaConsumer(
                settings.CURRENCY_UPDATE_TOPIC,
                loop=settings.loop(),
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=settings.CURRENCY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = CurrencyUpdate.parse_raw(msg.value)
            query = Currency.update() \
                .where(Currency.c.id == payload.id) \
                .values(payload.dict(exclude_none=True))
            return await db.execute(query=query)
    finally:
        await consumer.stop()


async def deleteCurrency(
        settings: kafkaConfig.Settings = kafkaConfig.getSettings()
):

    consumer = AIOKafkaConsumer(
                settings.CURRENCY_DELETE_TOPIC,
                loop=settings.loop(),
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=settings.CURRENCY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = CurrencyOut.parse_raw(msg.value)
            query = Currency.delete().where(Currency.c.id == payload.id)
            return await db.execute(query=query)
    finally:
        await consumer.stop()

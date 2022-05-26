from aiokafka import AIOKafkaConsumer
from db import Country, database as db
from configs.kafkaConfig import (COUNTRY_CREATE_TOPIC, 
    COUNTRY_UPDATE_TOPIC, COUNTRY_DELETE_TOPIC,
    KAFKA_BOOTSTRAP_SERVERS, COUNTRY_CONSUMER_GROUP, loop)
from schemas import CountryOut, CountryUpdate, CountryIn
import json


async def createCountry():
    consumer = AIOKafkaConsumer(COUNTRY_CREATE_TOPIC,
                                loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=COUNTRY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = CountryIn.parse_raw(msg.value)
            query = Country.insert().values(dict(payload))
            await db.execute(query=query)
    finally:
        await consumer.stop()
   

async def getCountry(countryName: str):
    query = Country.select()
    return await db.fetch_one(query=query, values={"countryName": countryName})


async def updateCountry():
    consumer = AIOKafkaConsumer(COUNTRY_UPDATE_TOPIC,
                                loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, 
                                group_id=COUNTRY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = CountryUpdate.parse_raw(msg.value)
            query = Country.update().where(Country.c.id == payload.id).values(dict(payload))
            await db.execute(query=query)
    finally:
        await consumer.stop()
    

async def deleteCountry():
    consumer = AIOKafkaConsumer(COUNTRY_DELETE_TOPIC,
                                loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=COUNTRY_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            payload = CountryOut.parse_raw(msg.value)
            query = Country.delete().where(Country.c.id == payload.id)
            return await db.execute(query=query)
    finally:
        await consumer.stop()

def encodeToJson(payload):
    return json.dumps(json.loads(payload.json())).encode("utf-8")
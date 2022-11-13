from db import Country, database as db

from aiokafka import AIOKafkaConsumer

from configs.kafkaConfig import (
    COUNTRY_DELETE_TOPIC,
    KAFKA_BOOTSTRAP_SERVERS,
    COUNTRY_CONSUMER_GROUP,
    loop
)

import schemas

import json


async def createCountry(payload: schemas.CountryIn):
    query = Country.insert().values(dict(payload))
    await db.execute(query=query)


async def getCountry(countryName: str):
    query = Country.select().where()
    return await db.fetch_one(query=query, values={"countryName": countryName})


async def getAllCountry():
    query = Country.select()
    return await db.fetch_all(query=query)


async def updateCountry(payload: schemas.CountryUpdate):
    query = Country.update().where(Country.c.id == payload.id).values(dict(payload))
    await db.execute(query=query)
    

async def deleteCountry(payload: schemas.CountryOut):
            query = Country.delete().where(Country.c.id == payload.id)
            return await db.execute(query=query)\

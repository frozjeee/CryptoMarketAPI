from typing import Optional
from fastapi import APIRouter, Header
from aiokafka import AIOKafkaProducer
from configs.kafkaConfig import (
        loop, KAFKA_BOOTSTRAP_SERVERS, COUNTRY_CREATE_TOPIC,
        COUNTRY_DELETE_TOPIC,COUNTRY_UPDATE_TOPIC)
from configs.config import (forbiddenException)
from schemas import CountryIn, CountryOut, CountryUpdate
import json
import authorization
import crud


router = APIRouter()


@router.get("/{countryName}")
async def getCountry(countryName: str):
    return await crud.getCountry(countryName)


@router.post("/")
async def createCountry(
        currency: CountryIn,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = json.dumps(currency.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=COUNTRY_CREATE_TOPIC, value=currencyJson)
    finally:
        await producer.stop()


@router.patch("/")
async def updateCountry(
        currency: CountryUpdate,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = crud.encodeToJson(currency)
        await producer.send_and_wait(topic=COUNTRY_UPDATE_TOPIC, value=currencyJson)
    finally:
        await producer.stop()


@router.delete("/")
async def deleteCurrency(
        currency: CountryOut,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = json.dumps(currency.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=COUNTRY_DELETE_TOPIC, value=currencyJson)
    finally:
        await producer.stop()




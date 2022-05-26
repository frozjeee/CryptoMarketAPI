from typing import Optional
from fastapi import APIRouter, Header
from aiokafka import AIOKafkaProducer
from configs.kafkaConfig import (
    loop, KAFKA_BOOTSTRAP_SERVERS, CURRENCY_CREATE_TOPIC, 
    CURRENCY_DELETE_TOPIC, CURRENCY_UPDATE_TOPIC)
from configs.config import (forbiddenException)
from schemas import CurrencyIn, CurrencyOut, CurrencyUpdate
import json
import authorization
import crud


router = APIRouter()


@router.get("/{currencyName}")
async def getCurrency(currencyName: str):
    return await crud.getCurrency(currencyName)


@router.post("/")
async def createCurrency(
        payload: CurrencyIn, 
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = crud.encodeToJson(payload)
        await producer.send_and_wait(topic=CURRENCY_CREATE_TOPIC, value=currencyJson)
    finally:
        await producer.stop()


@router.patch("/")
async def updateCurrency(
        payload: CurrencyUpdate,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = crud.encodeToJson(payload)
        await producer.send_and_wait(topic=CURRENCY_UPDATE_TOPIC, value=currencyJson)
    finally:
        await producer.stop()


@router.delete("/")
async def deleteCurrency(
        payload: CurrencyOut,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = crud.encodeToJson(payload)
        await producer.send_and_wait(topic=CURRENCY_DELETE_TOPIC, value=currencyJson)
    finally:
        await producer.stop()




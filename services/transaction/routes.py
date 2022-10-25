from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from aiokafka import AIOKafkaProducer
import configs.kafkaConfig as kafkaConfig
import configs.config as config
from schemas import WalletIn
import authorization
import crud


router = APIRouter()


@router.get("/{wallet}/")
async def getWallet(wallet: str):
    return await crud.getWallet(wallet)
    

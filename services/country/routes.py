from typing import Optional
from fastapi import APIRouter, Header
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
        country: CountryIn,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException
    crud.createCountry(country)
    

@router.patch("/")
async def updateCountry(
        currency: CountryUpdate,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException



@router.delete("/")
async def deleteCurrency(
        currency: CountryOut,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise forbiddenException




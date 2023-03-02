from fastapi import APIRouter, Depends

from services.user.models import User
from services.auth.deps import getAdminUser
from services.currency import crud, schemas


router = APIRouter()


@router.get("/{currencyId}/", response_model=schemas.CurrencyOut)
async def getCurrency(currencyId: int):
    return await crud.getCurrency(currencyId)


@router.get("/")
async def getCurrencies():
    return await crud.getCurrencies()


@router.post("/")
async def createCurrency(
    currencyIn: schemas.CurrencyIn, adminUser: User = Depends(getAdminUser)
):
    await crud.createCurrency(currencyIn)


@router.patch("/{currencyId}/")
async def updateCurrency(
    currency: schemas.CurrencyUpdate, adminUser: User = Depends(getAdminUser)
):
    await crud.updateCurrency(currency)


@router.delete("/{currencyId}/")
async def deleteCurrency(currencyId: int, adminUser: User = Depends(getAdminUser)):
    await crud.deleteCurrency(currencyId)

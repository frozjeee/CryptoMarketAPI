from typing import List

from fastapi import APIRouter, Depends, Response, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from services.user.models import User
from services.db.deps import get_db_session
from services.auth.deps import getAdminUser
from services.currency import crud, schemas


router = APIRouter()


@router.get("/{pk}/history/")
async def getCurrency(
    db: AsyncSession = Depends(get_db_session),
    *,
    pk: int
):
    res = await crud.getCurrencyHistory(db, pk)
    all_res = [i for i in res]
    return all_res


@router.get("/", response_model=List[schemas.CurrencyOut])
async def getCurrencies(
    *,
    db: AsyncSession = Depends(get_db_session),
    limit: int = Query(None)
):
    return await crud.getCurrencies(db, limit)


@router.post("/", response_model=schemas.CurrencyOut)
async def createCurrency(
    db: AsyncSession = Depends(get_db_session),
    *,
    currencyIn: schemas.CurrencyIn,
    adminUser: User = Depends(getAdminUser)
):
    return await crud.createCurrency(db, currencyIn)


@router.patch("/{pk}/")
async def updateCurrency(
    db: AsyncSession = Depends(get_db_session),
    *,
    pk: int,
    currency: schemas.CurrencyUpdate, adminUser: User = Depends(getAdminUser)
):
    currency = await crud.getCurrency(db, pk)
    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency does not exist"
            )
    await crud.updateCurrency(db, pk, currency)


@router.delete("/{pk}/")
async def deleteCurrency(
    db: AsyncSession = Depends(get_db_session),
    *,
    pk: int,
    adminUser: User = Depends(getAdminUser)):
    currency = await crud.getCurrency(db, pk)
    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency does not exist"
            )
    await crud.deleteCurrency(db, pk)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

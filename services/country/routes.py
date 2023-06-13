from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.country import crud, schemas
from services.db.deps import get_db_session


router = APIRouter()


@router.get("/", response_model=List[schemas.CountrySchema])
async def getCountries(
    db: AsyncSession = Depends(get_db_session),
):
    return await crud.getAllCountries(db)

from typing import List
from fastapi import APIRouter

from services.country import crud, schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.CountrySchema])
async def getCountries():
    return await crud.getAllCountries()

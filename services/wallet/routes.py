from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.db.deps import get_db_session
from services.user.models import User
from services.auth.deps import getCurrentUser
from services.wallet import crud, schemas


router = APIRouter()


@router.get("/{pk}", response_model=List[schemas.WalletOut])   
async def getWallet(
    *,
    db: AsyncSession = Depends(get_db_session),
    pk: int
):
    return await crud.getWallet(db, pk)

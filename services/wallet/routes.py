from fastapi import APIRouter, Depends

from services.user.models import User
from services.auth.deps import getCurrentUser
from services.wallet import crud


router = APIRouter()


@router.get("/{userId}/")
async def getWallet(userId: int, user: User = Depends(getCurrentUser)):
    return await crud.getWallet(userId)

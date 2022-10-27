from fastapi import APIRouter, status, Response
from services.wallet.schemas import WalletTopUp
import crud


router = APIRouter()


@router.get("/{wallet}/")
async def getWallet(wallet: str):
    return await crud.getWallet(wallet)


@router.put("/{wallet}/")
async def topUpWallet(walletTopUp: WalletTopUp):
    await crud.topUpWallet(walletTopUp)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

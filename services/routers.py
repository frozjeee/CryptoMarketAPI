from fastapi import APIRouter

from wallet.routes import router as walletRouter
from auth.routes import router as authRouter
from currency.routes import router as currencyRouter
from country.routes import router as countryRouter
from order.routes import router as orderRouter
from transaction.routes import router as transactionRouter
from user.routes import router as userRouter


router = APIRouter()


router.include_router(walletRouter, prefix="/wallet")
router.include_router(authRouter, prefix="/auth")
router.include_router(currencyRouter, prefix="/currency")
router.include_router(countryRouter, prefix="/country")
router.include_router(orderRouter, prefix="/router")
router.include_router(transactionRouter, prefix="/transaction")
router.include_router(userRouter, prefix="/user")

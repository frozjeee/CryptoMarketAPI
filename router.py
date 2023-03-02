from fastapi import APIRouter

from services.wallet.routes import router as walletRouter
from services.auth.routes import router as authRouter
from services.currency.routes import router as currencyRouter
from services.country.routes import router as countryRouter
from services.order.routes import router as orderRouter

# from services.transaction.routes import router as transactionRouter
from services.user.routes import router as userRouter


router = APIRouter()


router.include_router(walletRouter, prefix="/wallet", tags=["wallet"])
router.include_router(authRouter, prefix="/auth", tags=["auth"])
router.include_router(currencyRouter, prefix="/currency", tags=["currency"])
router.include_router(countryRouter, prefix="/country", tags=["country"])
router.include_router(orderRouter, prefix="/router", tags=["order"])
# router.include_router(transactionRouter, prefix="/transaction", tags=["transaction"])
router.include_router(userRouter, prefix="/user", tags=["user"])

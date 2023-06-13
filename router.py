from fastapi import APIRouter

from services.wallet.routes import router as walletRouter
from services.auth.routes import router as authRouter
from views.router import router as viewsRouter
from services.currency.routes import router as currencyRouter
from services.country.routes import router as countryRouter
from services.order.routes import router as orderRouter
from services.user.routes import router as userRouter


router = APIRouter()


router.include_router(viewsRouter, tags=["router"])
router.include_router(authRouter, prefix="/auth", tags=["auth"])
router.include_router(currencyRouter, prefix="/currency", tags=["currency"])
router.include_router(countryRouter, prefix="/country", tags=["country"])
router.include_router(orderRouter, prefix="/order", tags=["order"])
router.include_router(userRouter, prefix="/user", tags=["user"])
router.include_router(walletRouter, prefix="/wallet", tags=["user"])

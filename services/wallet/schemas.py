from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

from services.currency.schemas import CurrencyOut


class WalletOut(BaseModel):
    currency: CurrencyOut
    quantity: Optional[Decimal] = Field()
    created_at: Optional[datetime] = Field()

    class Config:
        orm_mode = True


class WalletUpdate(BaseModel):
    user_id: int = Field()
    currency_id: int = Field()
    quantity: Optional[Decimal] = Field()

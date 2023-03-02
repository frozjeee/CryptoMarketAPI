from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class WalletIn(BaseModel):
    userId: int = Field()
    currencyId: int = Field()
    quantity: Optional[Decimal] = Field()
    created_at: Optional[datetime] = Field()


class WalletUpdate(BaseModel):
    user_id: int = Field()
    currency_id: int = Field()
    quantity: Optional[Decimal] = Field()

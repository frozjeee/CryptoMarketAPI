from typing import Optional
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel

from services.order import OrderTypeEnum


class OrderIn(BaseModel):
    currency_id: int
    type: OrderTypeEnum
    price: Decimal
    quantity: Decimal


class OrderOut(OrderIn):
    id: int
    status: str

    class Config:
        orm_mode = True


class UserVerified(BaseModel):
    id: int
    verified: bool
    updated_at: Optional[datetime]

from typing import Optional
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class OrderIn(BaseModel):
    id: Optional[int]
    user_id: int
    currency_id: int
    type: str
    price: Decimal
    quantity: Decimal
    status: str
    main_currency: str
    ordered_at: Optional[datetime]


class OrderOut(BaseModel):
    id: int


class UserVerify(BaseModel):
    verified: bool
    updated_at: Optional[datetime]

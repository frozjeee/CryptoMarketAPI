from typing import Optional

from pydantic import BaseModel
from decimal import Decimal


class CurrencyIn(BaseModel):
    name: str
    code: str
    quantity: Decimal
    price: Decimal


class CurrencyOut(CurrencyIn):
    id: int

    class Config:
        orm_mode = True


class CurrencyUpdate(BaseModel):
    id: int
    code: Optional[str]
    name: Optional[str]
    market_cap: Optional[Decimal]
    quantity: Optional[Decimal]
    price: Optional[Decimal]

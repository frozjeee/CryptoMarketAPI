from typing import Optional

from pydantic import BaseModel, Field
from decimal import Decimal


class CurrencyIn(BaseModel):
    name: str
    code: str
    market_cap: Optional[Decimal]
    quantity: Decimal
    price: Decimal


class CurrencyOut(BaseModel):
    id: int


class CurrencyUpdate(BaseModel):
    id: int
    code: Optional[str]
    name: Optional[str]
    market_cap: Optional[Decimal]
    quantity: Optional[Decimal]
    price: Optional[Decimal]

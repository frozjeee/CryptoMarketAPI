from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CurrencyIn(BaseModel):
    id: Optional[UUID]
    name: str
    code: str
    market_cap: Optional[float]
    quantity: float
    price: float


class CurrencyOut(BaseModel):
    id: UUID


class CurrencyUpdate(BaseModel):
    id: UUID
    code: Optional[str]
    name: Optional[str]
    market_cap: Optional[float]
    quantity: Optional[float]
    price: Optional[float]


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]
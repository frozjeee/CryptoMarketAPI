from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class CurrencyIn(BaseModel):
    id: UUID = uuid4()
    name: str
    code: str
    market_cap: float
    price: float


class CurrencyOut(BaseModel):
    id: UUID


class CurrencyUpdate(BaseModel):
    id: UUID
    code: Optional[str]
    name: Optional[str]
    market_cap: Optional[float]
    price: Optional[float]


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]
from decimal import Decimal
from uuid import UUID
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class WalletIn(BaseModel):
    id: Optional[UUID]
    quantity: Optional[Decimal] = 0
    created_at: Optional[datetime]


class WalletQuantityInfo(BaseModel):
    id: Optional[UUID]
    quantity: Optional[Decimal]


class CurrencyInfo(BaseModel):
    id: Optional[UUID]
    code: Optional[str]
    name: Optional[str]


class WalletInfo(BaseModel):
    Wallet: WalletQuantityInfo
    Currency: CurrencyInfo


class WalletUpdate(BaseModel):
    id: UUID
    user_id: UUID
    currency_id: UUID
    quantity: Optional[Decimal]

    @validator("quantity")
    def validate_quantity(cls, value: Decimal):
        if value >= 0:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Less than zero")


class WalletOut(BaseModel):
    id: UUID


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]

class WalletTopUp(BaseModel):
    user_id: UUID
    currency_id: UUID
    quantity: Decimal

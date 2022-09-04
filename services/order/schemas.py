from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class OrderIn(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    currency_id: UUID
    type: str
    price: float
    quantity: float
    status: str
    ordered_at: Optional[datetime]


class OrderOut(BaseModel):
    id: UUID


class UserVerify(BaseModel):
    verified: bool
    updated_at: Optional[datetime]


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class WalletIn(BaseModel):
    id: Optional[UUID]
    quantity: Optional[float] = 0
    created_at: Optional[datetime]
    

class WalletUpdate(BaseModel):
    id: UUID
    user_id: UUID
    currency_id: UUID
    quantity: Optional[float]


class WalletOut(BaseModel):
    id: UUID


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]
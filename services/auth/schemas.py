from uuid import uuid4, UUID
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class UserIn(BaseModel):
    id: UUID = uuid4()
    name: str
    is_superuser: bool = False
    password: str
    verified: Optional[bool] = False
    email: EmailStr
    birthdate: date
    country_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]

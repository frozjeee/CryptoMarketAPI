from uuid import UUID, uuid4
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
    created_at: Optional[datetime] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    updated_at: Optional[datetime] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")


class CountryIn(BaseModel):
    id: int
    name: str
    code: str


class CountryOut(BaseModel):
    id: int


class CountryUpdate(BaseModel):
    id: int
    code: Optional[str]
    name: Optional[str]


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]
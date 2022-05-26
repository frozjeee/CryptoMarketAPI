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


class UserShow(BaseModel):
    id: UUID
    name: str
    is_superuser: bool
    verified: bool
    email: EmailStr
    birthdate: date
    country_id: int
    created_at: datetime


class UserOut(BaseModel):
    id: UUID


class UserUpdate(BaseModel):
    id: UUID
    name: Optional[str]
    updated_at: Optional[datetime] = datetime.today()


class UserVerify(BaseModel):
    verified: bool
    updated_at: Optional[datetime] = datetime.today()


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]
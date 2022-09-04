from uuid import UUID, uuid4
from fastapi import Form, UploadFile
from pydantic import BaseModel, EmailStr
from typing import Any, Optional
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
    updated_at: Optional[datetime]


class UserVerify(BaseModel):
    id: UUID
    frontPage: str
    backPage: str
    userFace: str


class UserId(BaseModel):
    id: UUID


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]
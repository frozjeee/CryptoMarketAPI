import base64
from decimal import Decimal

from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

from services.country.schemas import CountrySchema


class UserInSchema(BaseModel):
    name: str
    password: str
    email: EmailStr
    birthdate: date
    country_id: int


class UserOutSchema(UserInSchema):
    id: int
    is_superuser: bool
    email: EmailStr
    balance: Decimal
    verified: bool
    birthdate: date
    country: CountrySchema

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    id: int
    verified: Optional[bool]
    name: Optional[str]


class UserVerify(BaseModel):
    frontPage: UploadFile
    backPage: UploadFile
    userFace: UploadFile

    @classmethod
    def asForm(
        cls,
        frontPage: UploadFile = File(...),
        backPage: UploadFile = File(...),
        userFace: UploadFile = File(...),
    ):
        return cls(frontPage=frontPage, backPage=backPage, userFace=userFace)

    async def toBase64(self):
        frontPage = await self.frontPage.read()
        backPage = await self.backPage.read()
        userFace = await self.userFace.read()
        self.frontPage = base64.b64encode(frontPage).decode("utf-8")
        self.backPage = base64.b64encode(backPage).decode("utf-8")
        self.userFace = base64.b64encode(userFace).decode("utf-8")

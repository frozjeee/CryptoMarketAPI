import base64
from uuid import UUID, uuid4
from fastapi import Form, UploadFile
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
    is_superuser: Optional[bool]
    verified: Optional[bool]
    email: Optional[EmailStr]
    birthdate: Optional[date]
    country_id: Optional[int]
    updated_at: Optional[datetime] = datetime.today()


class UserVerify(BaseModel):
    id: UUID
    frontPage: UploadFile
    backPage: UploadFile
    userFace: UploadFile

    @classmethod
    def asForm(
        cls,
        id: UUID = Form(...),
        frontPage: UploadFile = Form(...),
        backPage: UploadFile = Form(...),
        userFace: UploadFile = Form(...)
    ):
        return cls(id=id, frontPage=frontPage, backPage=backPage, userFace=userFace)

    async def toBase64(self):
        frontPage = await self.frontPage.read()
        backPage = await self.backPage.read()
        userFace = await self.userFace.read()
        self.frontPage = base64.b64encode(frontPage)
        self.backPage = base64.b64encode(backPage)
        self.userFace = base64.b64encode(userFace)


class UserId(BaseModel):
    id: UUID


class TokenData(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]
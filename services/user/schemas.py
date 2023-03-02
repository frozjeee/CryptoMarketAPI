import base64
from fastapi import Form, UploadFile
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class UserIn(BaseModel):
    name: str
    password: str
    is_superuser: Optional[bool]
    verified: Optional[bool]
    email: EmailStr
    birthdate: date
    country_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserOut(UserIn):
    id: int


class UserVerify(BaseModel):
    id: Optional[int]
    frontPage: UploadFile
    backPage: UploadFile
    userFace: UploadFile

    @classmethod
    def asForm(
        cls,
        id: id = Form(...),
        frontPage: UploadFile = Form(...),
        backPage: UploadFile = Form(...),
        userFace: UploadFile = Form(...),
    ):
        return cls(id=id, frontPage=frontPage, backPage=backPage, userFace=userFace)

    async def toBase64(self):
        frontPage = await self.frontPage.read()
        backPage = await self.backPage.read()
        userFace = await self.userFace.read()
        self.frontPage = base64.b64encode(frontPage)
        self.backPage = base64.b64encode(backPage)
        self.userFace = base64.b64encode(userFace)

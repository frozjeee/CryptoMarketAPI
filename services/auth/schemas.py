from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class TokenData(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_superuser: bool
    exp: Optional[datetime]

    class Config:
        orm_mode = True

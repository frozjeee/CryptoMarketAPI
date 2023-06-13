from pydantic import BaseModel, Field


class CountrySchema(BaseModel):
    id: int = Field()
    name: str = Field()
    code: str = Field()

    class Config:
        orm_mode = True

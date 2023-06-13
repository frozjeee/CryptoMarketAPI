from sqlalchemy import Column, Integer, String

from services.db.db import Model


class Country(Model):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, unique=True)
    code = Column(String(10))
    name = Column(String(50), unique=True)

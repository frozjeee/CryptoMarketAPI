from sqlalchemy import DateTime, Boolean, Column, Date, Integer, \
    String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from services.db.db import Model
from services.common import timezone


class User(Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, unique=True)
    is_superuser = Column(Boolean, default=True)
    balance = Column(DECIMAL, default=0)
    email = Column(String(250), unique=True)
    name = Column(String(250))
    password = Column(String(250))
    birthdate = Column(Date)
    country_id = Column(Integer, ForeignKey("country.id"))
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=timezone.now)
    updated_at = Column(DateTime, default=timezone.now, onupdate=timezone.now)

    country = relationship("Country", backref="users")

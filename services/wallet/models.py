from sqlalchemy import (
    DateTime,
    Column,
    DECIMAL,
    UniqueConstraint,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship

from services.common import timezone
from services.db.db import Model


class Wallet(Model):
    __tablename__ = "wallet"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    currency_id = Column(Integer, ForeignKey("currency.id"), primary_key=True)
    quantity = Column(DECIMAL, default=0)
    created_at = Column(DateTime, default=timezone.now)
    updated_at = Column(DateTime, default=timezone.now, onupdate=timezone.now)

    currency = relationship("Currency", backref="wallet")
    __table_args__ = (UniqueConstraint("user_id", "currency_id", name="uix_wallet_user_id_currency_id"), )

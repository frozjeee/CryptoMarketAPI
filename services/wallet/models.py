from sqlalchemy import (
    DateTime,
    Column,
    DECIMAL,
    Table,
    UniqueConstraint,
    Boolean,
    Integer,
)

from services.common import timezone
from services.db.db import metadata


Wallet = Table(
    "wallet",
    metadata,
    Column(Integer, name="user_id", primary_key=True),
    Column(Integer, name="currency_id", primary_key=True),
    Column("quantity", DECIMAL),
    Column("created_at", DateTime, default=timezone.now),
    Column("updated_at", DateTime, default=timezone.now, onupdate=timezone.now),
    UniqueConstraint("user_id", "currency_id", name="uix_wallet_user_id_currency_id"),
)

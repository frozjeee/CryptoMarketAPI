from sqlalchemy import DateTime, Boolean, Column, Date, Integer, String, Table, ForeignKey

from services.common import timezone
from services.db.db import metadata


User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("is_superuser", Boolean, default=True),
    Column("email", String(250), unique=True),
    Column("name", String(250)),
    Column("password", String(250)),
    Column("birthdate", Date),
    Column("country_id", Integer, ForeignKey("country.id")),
    Column("verified", Boolean),
    Column("currency_id", Integer, ForeignKey("currency.id")),
    Column("created_at", DateTime, default=timezone.now),
    Column("updated_at", DateTime, default=timezone.now, onupdate=timezone.now)
)

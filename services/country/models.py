from sqlalchemy import Column, Integer, String, Table

from services.db.db import metadata


Country = Table(
    "country",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("code", String(10)),
    Column("name", String(50), unique=True),
)

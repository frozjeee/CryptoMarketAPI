from sqlalchemy import (Column, Integer, MetaData, String, Table)
from configs.config import DATABASE_URL, AUTH_DATABASE_URL
import databases


database = databases.Database(DATABASE_URL)
auth_database = databases.Database(AUTH_DATABASE_URL)
metadata = MetaData()


Country = Table(
    'country',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False, unique=True),
    Column('code', String(10), nullable=False),
    Column('name', String(50), nullable=False, unique=True),
)




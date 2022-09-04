from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (TIMESTAMP, Boolean, Column, Date, 
                        Integer, MetaData, String, Table)
from configs.config import getSettings
import uuid
import databases


settings = getSettings()

database = databases.Database(settings.DATABASE_URL)
metadata = MetaData()

User = Table(
    'user',
    metadata,
    Column(UUID(as_uuid=True), name='id', primary_key=True, default=uuid.uuid4(), nullable=False, unique=True),
    Column('is_superuser', Boolean, default=True, nullable=False),
    Column('email', String(250), unique=True, nullable=False),
    Column('name', String(250), nullable=False),
    Column('password', String(250), nullable=False),
    Column('birthdate', Date, nullable=False),
    Column('country_id', Integer, nullable=False),
    Column('verified', Boolean, default=True),
    Column('created_at', TIMESTAMP, nullable=False, default=datetime.today()),
    Column('updated_at', TIMESTAMP, nullable=False, default=datetime.today())
)


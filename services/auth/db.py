from sqlalchemy import MetaData
from configs.config import DATABASE_URL
import databases


database = databases.Database(DATABASE_URL)

metadata = MetaData()

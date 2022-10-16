from configs.config import getSettings
import databases


settings = getSettings()

database = databases.Database(settings.DATABASE_URL)

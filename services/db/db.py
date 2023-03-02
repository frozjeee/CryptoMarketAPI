import databases
from sqlalchemy import MetaData

from config.config import settings


db = databases.Database(settings.DATABASE_URL)
metadata = MetaData()

from services.currency.models import *
from services.user.models import *
from services.country.models import *
from services.wallet.models import *
from services.order.models import *

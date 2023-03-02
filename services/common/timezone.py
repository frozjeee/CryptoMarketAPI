from datetime import datetime

import pytz


def now():
    return datetime.now(tz=pytz.timezone(False)).replace(tzinfo=None)

import json
from decimal import Decimal
from typing import Union
from datetime import date, datetime



def dt_as_isoformat(obj: Union[datetime, date]) -> str:  # noqa
    """Фоматирует даты в ISO-формат

    :param obj: дата
    :type obj: datetime или date
    :return: форматированную строку даты
    :rtype: str
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def serialize_dict_as_str(data: dict) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        cls=DecimalEncoder
    )


def serialize_dict(data: dict) -> bytes:
    """Сериализует словарь в json

    :param data: словарь с данными
    :type data: dict
    :return: json
    :rtype: bytes
    """
    return serialize_dict_as_str(data=data).encode(encoding="utf-8")


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

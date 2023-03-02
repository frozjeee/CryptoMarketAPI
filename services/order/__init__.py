from enum import Enum


class OrderStatusEnum(str, Enum):
    pending = "pending"
    done = "done"
    cancelled = "cancelled"


class OrderTypeEnum(str, Enum):
    buy = "buy"
    sell = "sell"

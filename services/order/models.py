from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship

from services.order import OrderStatusEnum, OrderTypeEnum
from services.db.db import Model
from services.common import timezone

class Order(Model):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("user.id"))
    buyer_id  = Column(Integer, ForeignKey("user.id"))
    currency_id = Column(Integer, ForeignKey("currency.id"))
    type = Column(Enum(OrderTypeEnum))
    price = Column(DECIMAL)
    init_quantity = Column(DECIMAL)
    quantity = Column(DECIMAL)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.pending)
    created_at = Column(DateTime, default=timezone.now)
    created_by = Column(Integer, ForeignKey("user.id"))

    seller = relationship("User", backref="sell_orders", foreign_keys="Order.seller_id")
    buyer = relationship("User", backref="buy_orders", foreign_keys="Order.buyer_id")
    cleater = relationship("User", backref="creator", foreign_keys="Order.created_by")
    currency = relationship("Currency", backref="currency")

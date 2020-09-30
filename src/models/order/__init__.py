from enum import Enum
from sqlalchemy import Column, String, Integer, ForeignKey, Float, ARRAY
from sqlalchemy.orm import relationship

from src.models.base import NonDeletableModel


class OrderStatus(Enum):
    IDLE = "idle"
    REJECTED = "rejected"
    APPROVED = "approved"
    COMPLETED = "completed"


class Order(NonDeletableModel):
    __tablename__ = "order"

    user_name = Column(String(255), nullable=False)
    user_phone_number = Column(String(255), nullable=False)
    user_address = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", lazy="joined")
    promo_code_value = Column(String(60), nullable=False)
    promo_code_discount = Column(Integer, nullable=False)
    promo_code_amount = Column(Float, nullable=True)
    promo_code_products_ids = Column(ARRAY(Integer), item_type=Integer)
    items = relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete, delete-orphan",
        lazy="joined",
    )
    # statuses are: idle, approved, rejected, completed
    status = Column(String(60), default="idle", nullable=False)

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class OrderItem(BaseModel):
    __tablename__ = "order_item"

    order_id = Column(Integer, ForeignKey("order.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    product_price_per_item = Column(Integer, nullable=False)
    product_discount = Column(Integer, nullable=False)
    product_id = Column(
        Integer, ForeignKey("product.id", ondelete="SET NULL"), nullable=True
    )
    product = relationship("Product", lazy="joined")

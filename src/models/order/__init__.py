from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import NonDeletableModel


class Order(NonDeletableModel):
    __tablename__ = 'order'

    user_name = Column(String(255), nullable=False)
    user_phone_number = Column(String(255), nullable=False)
    user_address = Column(String(255), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=True
    )
    user = relationship("User", lazy='joined')
    promo_code_id = Column(
        Integer,
        ForeignKey('promo_code.id'),
        nullable=True
    )
    promo_code = relationship("PromoCode", lazy='joined')
    items = relationship(
        'OrderItem',
        backref='order',
        cascade="all, delete, delete-orphan",
        lazy="joined"
    )
    # statuses are: idle, approved, rejected, completed
    status = Column(String(60), default='idle', nullable=False)
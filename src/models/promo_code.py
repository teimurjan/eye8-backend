from sqlalchemy import Column, String, Integer, ARRAY, Boolean, Float
from src.models.base import NonDeletableModel

class PromoCode(NonDeletableModel):
    __tablename__ = "promo_code"

    value = Column(String(60), unique=True, nullable=False)
    discount = Column(Integer, nullable=False)
    amount = Column(Float, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    disable_on_use = Column(Boolean, nullable=False, default=True)
    products_ids = Column(ARRAY(Integer))

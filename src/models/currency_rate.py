from sqlalchemy import Column, String, Float
from src.models.base import BaseModel


class CurrencyRate(BaseModel):
    __tablename__ = "currency_rate"

    name = Column(String(10), nullable=False)
    value = Column(Float, nullable=False)

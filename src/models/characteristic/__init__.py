from sqlalchemy import Column, String
from src.models.base import BaseModel


class Characteristic(BaseModel):
    __tablename__ = "characteristic"

    name_en = Column(String(255), nullable=False)
    name_ru = Column(String(255), nullable=False)

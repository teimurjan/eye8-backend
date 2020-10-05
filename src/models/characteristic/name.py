from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.intl import IntlText


class CharacteristicName(IntlText):
    __tablename__ = "characteristic_name"

    value = Column(String(50), nullable=False)
    characteristic_id = Column(Integer, ForeignKey("characteristic.id"), nullable=False)

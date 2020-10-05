from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.intl import IntlText


class CharacteristicValueName(IntlText):
    __tablename__ = "characteristic_value_name"

    value = Column(String(50), nullable=False)
    characteristic_value_id = Column(
        Integer, ForeignKey("characteristic_value.id"), nullable=False
    )

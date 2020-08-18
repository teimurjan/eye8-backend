from sqlalchemy import Column, UnicodeText, Integer, ForeignKey
from src.models.intl import IntlText


class ProductTypeDescription(IntlText):
    __tablename__ = "product_type_description"

    value = Column(UnicodeText(), nullable=False)
    product_type_id = Column(
        Integer, ForeignKey("product_type.id"), nullable=False, index=True
    )

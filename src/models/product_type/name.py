from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.schema import Index
from src.models.intl import IntlText


class ProductTypeName(IntlText):
    __tablename__ = "product_type_name"
    __table_args__ = (Index("ix_product_type_name_value", "value",),)

    value = Column(String(255), nullable=False)
    product_type_id = Column(
        Integer, ForeignKey("product_type.id"), nullable=False, index=True
    )

from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.intl import IntlText


class ProductTypeName(IntlText):
    __tablename__ = 'product_type_name'

    value = Column(String(255), nullable=False)
    product_type_id = Column(
        Integer,
        ForeignKey(
            'product_type.id'
        ),
        nullable=False
    )

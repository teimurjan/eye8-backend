from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.intl import IntlText


class ProductTypeShortDescription(IntlText):
    __tablename__ = 'product_type_short_description'

    value = Column(String(1000), nullable=False)
    product_type_id = Column(
        Integer,
        ForeignKey(
            'product_type.id'
        ),
        nullable=False,
        index=True
    )

from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.base import BaseModel


class ProductTypeInstagramLink(BaseModel):
    __tablename__ = 'product_type_instagram_link'

    link = Column(String(255), nullable=False)
    product_type_id = Column(
        Integer,
        ForeignKey(
            'product_type.id'
        ),
        nullable=False,
        index=True
    )

from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.base import BaseModel


class ProductImage(BaseModel):
    __tablename__ = "product_image"

    image = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, index=True)

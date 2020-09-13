from sqlalchemy import Column, String, Integer, ForeignKey, orm
from src.models.base import NonDeletableModel


class Product(NonDeletableModel):
    __tablename__ = "product"

    discount = Column(Integer, default=0)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, default=0)
    product_type_id = Column(
        Integer, ForeignKey("product_type.id"), nullable=False, index=True
    )
    product_type = orm.relationship("ProductType", lazy="joined")
    images = orm.relationship(
        "ProductImage",
        backref="product",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )
    upc = Column(String, nullable=True, unique=True)

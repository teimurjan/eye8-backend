from sqlalchemy import Column, Integer, ForeignKey, orm
from sqlalchemy.ext.hybrid import hybrid_property
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

    @hybrid_property
    def total_price(self):
        return self.price * ((100 - self.discount) * 0.01)

    @total_price.expression
    def total_price(cls):
        return cls.price * ((100 - cls.discount) * 0.01)

    @hybrid_property
    def availability(self):
        return self.quantity > 0

    @availability.expression
    def availability(cls):
        return cls.quantity > 0

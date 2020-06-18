from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, String, Integer, ForeignKey, orm, func
from src.models.base import NonDeletableModel


class Product(NonDeletableModel):
    __tablename__ = 'product'

    discount = Column(Integer, default=0)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, default=0)
    product_type_id = Column(
        Integer,
        ForeignKey(
            'product_type.id'
        ),
        nullable=False
    )
    product_type = orm.relationship('ProductType', lazy='joined')
    images = orm.relationship(
        'ProductImage',
        backref='product',
        lazy='joined',
        cascade="all, delete, delete-orphan"
    )
    upc = Column(String, nullable=True, unique=True)

    @hybrid_property
    def calculated_price(self):
        return round(self.price * ((100 - self.discount) * 0.01))

    @calculated_price.expression
    def calculated_price(cls):
        return cls.price * ((100 - cls.discount) * 0.01)

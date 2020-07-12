from operator import and_

from sqlalchemy import Column, ForeignKey, Integer, String, Table, orm
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import case, exists, select

from src.models.base import BaseModel, NonDeletableModel
from src.models.product import Product

ProductTypeXCategoryTable = Table(
    'product_type_x_category',
    BaseModel.metadata,
    Column('product_type_id', Integer, ForeignKey(
        'product_type.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey(
        'category.id'), primary_key=True)
)

class ProductType(NonDeletableModel):
    __tablename__ = 'product_type'

    names = orm.relationship(
        'ProductTypeName',
        backref='product_type',
        lazy='joined',
        cascade="all, delete, delete-orphan"
    )

    instagram_links = orm.relationship(
        'ProductTypeInstagramLink',
        backref='product_type',
        lazy='joined',
        cascade="all, delete, delete-orphan"
    )
    descriptions = orm.relationship(
        'ProductTypeDescription',
        backref='product_type',
        lazy='joined',
        cascade="all, delete, delete-orphan"
    )
    short_descriptions = orm.relationship(
        'ProductTypeShortDescription',
        backref='product_type',
        lazy='joined',
        cascade="all, delete, delete-orphan"
    )
    products = orm.relationship(
        'Product',
        lazy='select',
    )
    image = Column(String(255), nullable=True)
    categories = orm.relationship(
        'Category',
        secondary=ProductTypeXCategoryTable,
        lazy='joined',
        backref=orm.backref('product_types', lazy='joined')
    )
    slug = Column(String(255), nullable=False, unique=True)

    def __getitem__(self, key):
        if key == 'names':
            return self.names
        if key == 'descriptions':
            return self.descriptions
        if key == 'short_descriptions':
            return self.short_descriptions
        if key == 'instagram_links':
            return self.instagram_links

        return super().__getitem__(key)

    @hybrid_property
    def is_available(self):
        for product in self.products:
            if product.quantity > 0:
                return True
        return False

    @is_available.expression
    def is_available(cls):
        return (
            select([
                case(
                    [
                        (
                            exists()
                            .where(and_(Product.product_type_id == cls.id, Product.quantity > 0))
                            .correlate(cls),
                            True
                        )
                    ],
                    else_=False,
                )
                .label("is_available")
            ])
            .label('number_of_available_products')
        )

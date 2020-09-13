from src.models.product import Product
from sqlalchemy import Column, ForeignKey, Integer, String, Table, orm
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import and_, case, exists, select
from sqlalchemy.sql.functions import func

from src.models.base import BaseModel, NonDeletableModel

ProductTypeXCategoryTable = Table(
    "product_type_x_category",
    BaseModel.metadata,
    Column(
        "product_type_id",
        Integer,
        ForeignKey("product_type.id"),
        primary_key=True,
        index=True,
    ),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
)


class ProductType(NonDeletableModel):
    __tablename__ = "product_type"

    names = orm.relationship(
        "ProductTypeName",
        backref="product_type",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )

    instagram_links = orm.relationship(
        "ProductTypeInstagramLink",
        backref="product_type",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )
    descriptions = orm.relationship(
        "ProductTypeDescription",
        backref="product_type",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )
    short_descriptions = orm.relationship(
        "ProductTypeShortDescription",
        backref="product_type",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )
    products = orm.relationship("Product", lazy="joined",)
    image = Column(String(255), nullable=True)
    categories = orm.relationship(
        "Category",
        secondary=ProductTypeXCategoryTable,
        lazy="joined",
        backref=orm.backref("product_types"),
    )
    slug = Column(String(255), nullable=False, unique=True)

    def __getitem__(self, key):
        if key == "names":
            return self.names
        if key == "descriptions":
            return self.descriptions
        if key == "short_descriptions":
            return self.short_descriptions
        if key == "instagram_links":
            return self.instagram_links

        return super().__getitem__(key)

    @hybrid_property
    def min_price(self):
        return min(
            [
                product.price * ((100 - product.discount) * 0.01)
                for product in self.products
            ]
        )

    @min_price.expression
    def min_price(cls):
        return (
            select([func.min(Product.price * ((100 - Product.discount) * 0.01))])
            .where(Product.product_type_id == cls.id)
            .correlate(cls)
            .label("min_price")
        )

    @hybrid_property
    def availability(self):
        return len([product for product in self.products if product.quantity > 0])

    @availability.expression
    def availability(cls):
        return select(
            [
                case(
                    [
                        (
                            exists()
                            .where(
                                and_(
                                    Product.product_type_id == cls.id,
                                    Product.quantity > 0,
                                )
                            )
                            .correlate(cls),
                            True,
                        )
                    ],
                    else_=False,
                )
            ]
        ).label("availability")


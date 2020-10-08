from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    orm,
    select,
    func,
    case,
    exists,
    and_,
)
from sqlalchemy.ext.hybrid import hybrid_property

from src.models.base import BaseModel, NonDeletableModel
from src.models.product import Product

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
    products = orm.relationship(
        "Product",
        lazy="joined",
        primaryjoin="and_(ProductType.id == Product.product_type_id, or_(Product.is_deleted == False, Product.is_deleted == None))",
    )
    image = Column(String(255), nullable=True)
    categories = orm.relationship(
        "Category",
        secondary=ProductTypeXCategoryTable,
        lazy="subquery",
        backref=orm.backref("product_types"),
    )
    slug = Column(String(255), nullable=False, unique=True)

    @hybrid_property
    def products_min_price(self):
        return min([product.total_price for product in self.products])

    @products_min_price.expression
    def products_min_price(cls):
        return (
            select([func.min(Product.total_price)])
            .where(Product.product_type_id == cls.id)
            .correlate(cls)
            .label("products_min_price")
        )

    @hybrid_property
    def products_available(self):
        return len([product for product in self.products if product.available]) > 0

    @products_available.expression
    def products_available(cls):
        return select(
            [
                case(
                    [
                        (
                            exists()
                            .where(
                                and_(
                                    Product.product_type_id == cls.id,
                                    Product.available,
                                )
                            )
                            .correlate(cls),
                            True,
                        )
                    ],
                    else_=False,
                )
            ]
        ).label("products_available")

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


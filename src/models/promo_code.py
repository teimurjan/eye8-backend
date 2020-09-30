from sqlalchemy import Table, Column, String, Integer, ForeignKey, orm, Boolean, Float
from src.models.base import NonDeletableModel, BaseModel

ProductXPromoCodeTable = Table(
    "product_x_promo_code",
    BaseModel.metadata,
    Column(
        "product_id", Integer, ForeignKey("product.id"), primary_key=True, index=True
    ),
    Column("promo_code_id", Integer, ForeignKey("promo_code.id"), primary_key=True),
)


class PromoCode(NonDeletableModel):
    __tablename__ = "promo_code"

    value = Column(String(60), unique=True, nullable=False)
    discount = Column(Integer, nullable=False)
    amount = Column(Float, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    disable_on_use = Column(Boolean, nullable=False, default=True)
    products = orm.relationship(
        "Product",
        secondary=ProductXPromoCodeTable,
        backref=orm.backref("promo_codes"),
        lazy="selectin",
    )

from sqlalchemy import Table, Column, Integer, ForeignKey, orm, String
from src.models.base import BaseModel

ProductXFeatureValueTable = Table(
    "product_x_feature_value",
    BaseModel.metadata,
    Column(
        "product_id", Integer, ForeignKey("product.id"), primary_key=True, index=True
    ),
    Column(
        "feature_value_id",
        Integer,
        ForeignKey("feature_value.id"),
        primary_key=True,
        index=True,
    ),
)


class FeatureValue(BaseModel):
    __tablename__ = "feature_value"

    name_en = Column(String(255), nullable=False)
    name_ru = Column(String(255), nullable=False)
    feature_type_id = Column(
        Integer, ForeignKey("feature_type.id"), nullable=False, index=True
    )
    feature_type = orm.relationship("FeatureType", lazy="joined")
    products = orm.relationship(
        "Product",
        secondary=ProductXFeatureValueTable,
        lazy="select",
        backref=orm.backref("feature_values", lazy="joined"),
    )


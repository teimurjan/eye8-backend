from sqlalchemy import orm, Table, Integer, Column, ForeignKey, String
from src.models.base import BaseModel

ProductTypeXFeatureTypeTable = Table(
    "product_type_x_feature_type",
    BaseModel.metadata,
    Column(
        "product_type_id",
        Integer,
        ForeignKey("product_type.id"),
        primary_key=True,
        index=True,
    ),
    Column(
        "feature_type_id",
        Integer,
        ForeignKey("feature_type.id"),
        primary_key=True,
        index=True,
    ),
)


class FeatureType(BaseModel):
    __tablename__ = "feature_type"

    name_en = Column(String(255), nullable=False)
    name_ru = Column(String(255), nullable=False)
    feature_values = orm.relationship(
        "FeatureValue", lazy="select", cascade="all, delete, delete-orphan"
    )
    product_types = orm.relationship(
        "ProductType",
        secondary=ProductTypeXFeatureTypeTable,
        lazy="select",
        backref=orm.backref("feature_types", lazy="joined"),
    )

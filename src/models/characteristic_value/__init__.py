from sqlalchemy import Table, Column, Integer, ForeignKey, orm, String
from src.models.base import BaseModel

ProductTypeXCharacteristicValueTable = Table(
    "Product_type_x_characteristic_value",
    BaseModel.metadata,
    Column(
        "product_type_id",
        Integer,
        ForeignKey("product_type.id"),
        primary_key=True,
        index=True,
    ),
    Column(
        "characteristic_value_id",
        Integer,
        ForeignKey("characteristic_value.id"),
        primary_key=True,
        index=True,
    ),
)


class CharacteristicValue(BaseModel):
    __tablename__ = "characteristic_value"

    name_en = Column(String(255), nullable=False)
    name_ru = Column(String(255), nullable=False)

    characteristic_id = Column(
        Integer, ForeignKey("characteristic.id"), nullable=False, index=True
    )
    characteristic = orm.relationship("Characteristic", lazy="joined")
    product_types = orm.relationship(
        "ProductType",
        secondary=ProductTypeXCharacteristicValueTable,
        lazy="select",
        backref=orm.backref("characteristic_values", lazy="joined"),
    )

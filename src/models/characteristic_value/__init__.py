from sqlalchemy import Table, Column, Integer, ForeignKey, orm
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

    names = orm.relationship(
        "CharacteristicValueName",
        backref="characteristic_value",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )
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

    def __getitem__(self, key):
        if key == "names":
            return self.names

        return super().__getitem__(key)

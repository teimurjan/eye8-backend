from sqlalchemy import orm
from src.models.base import BaseModel


class Characteristic(BaseModel):
    __tablename__ = "characteristic"

    names = orm.relationship(
        "CharacteristicName",
        backref="characteristic",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )
    def __getitem__(self, key):
        if key == "names":
            return self.names

        return super().__getitem__(key)

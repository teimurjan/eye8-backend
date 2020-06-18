from sqlalchemy import Column, String, orm, Integer, ForeignKey, Float
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class IntlText(BaseModel):
    __abstract__ = True

    @declared_attr
    def language_id(cls):
        return Column(
            Integer,
            ForeignKey(
                'language.id'
            ),
            nullable=False
        )

    @declared_attr
    def language(cls):
        return relationship("Language", lazy='joined')



class Language(BaseModel):
    __tablename__ = 'language'

    name = Column(String(10), nullable=False, unique=True)

class CurrencyRate(BaseModel):
    __tablename__ = 'currency_rate'

    name = Column(String(10), nullable=False)
    value = Column(Float, nullable=False)

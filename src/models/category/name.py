from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.schema import Index
from src.models.intl import IntlText


class CategoryName(IntlText):
    __tablename__ = "category_name"
    __table_args__ = (Index("ix_category_name_value", "value",),)

    value = Column(String(50), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, index=True)

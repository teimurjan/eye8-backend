from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.intl import IntlText


class CategoryName(IntlText):
    __tablename__ = "category_name"

    value = Column(String(50), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

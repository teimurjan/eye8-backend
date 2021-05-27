from sqlalchemy import Column, String, Integer, ForeignKey, String
from src.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    name_en = Column(String(255), nullable=False)
    name_ru = Column(String(255), nullable=False)
    parent_category_id = Column(Integer, ForeignKey("category.id"), nullable=True, index=True)
    slug = Column(String(255), nullable=False, unique=True)
    
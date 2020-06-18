from sqlalchemy import Column, String, orm
from src.models.base import BaseModel


class Group(BaseModel):
    __tablename__ = 'group'

    name = Column(String(60), unique=True, nullable=False)

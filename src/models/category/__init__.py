from sqlalchemy import Column, String, Integer, ForeignKey, orm
from src.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'

    names = orm.relationship(
        'CategoryName',
        backref='category',
        lazy='joined',
        cascade="all, delete, delete-orphan"
    )
    product_types = orm.relationship('ProductType', lazy='select')
    parent_category_id = Column(
        Integer, ForeignKey('category.id'), nullable=True)
    slug = Column(String(255), nullable=False, unique=True)

    def __getitem__(self, key):
        if key == 'names':
            return self.names

        return super().__getitem__(key)

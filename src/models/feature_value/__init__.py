from sqlalchemy import Table, Column, String, Integer, ForeignKey, orm
from src.models.base import BaseModel

ProductXFeatureValueTable = Table(
    'product_x_feature_value',
    BaseModel.metadata,
    Column(
        'product_id',
        Integer,
        ForeignKey('product.id'),
        primary_key=True,
        index=True
    ),
    Column(
        'feature_value_id',
        Integer,
        ForeignKey('feature_value.id'),
        primary_key=True
    )
)


class FeatureValue(BaseModel):
    __tablename__ = 'feature_value'

    names = orm.relationship(
        'FeatureValueName',
        backref='feature_value',
        lazy='joined',
        cascade="all, delete, delete-orphan"
    )
    feature_type_id = Column(
        Integer,
        ForeignKey('feature_type.id'),
        nullable=False
    )
    feature_type = orm.relationship("FeatureType", lazy='joined')
    products = orm.relationship(
        'Product',
        secondary=ProductXFeatureValueTable,
        lazy='select',
        backref=orm.backref('feature_values', lazy='joined')
    )

    def __getitem__(self, key):
        if key == 'names':
            return self.names

        return super().__getitem__(key)

from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.intl import IntlText


class FeatureTypeName(IntlText):
    __tablename__ = 'feature_type_name'

    value = Column(String(50), nullable=False)
    feature_type_id = Column(
        Integer,
        ForeignKey(
            'feature_type.id'
        ),
        nullable=False
    )

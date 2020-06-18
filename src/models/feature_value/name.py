from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.intl import IntlText


class FeatureValueName(IntlText):
    __tablename__ = 'feature_value_name'

    value = Column(String(50), nullable=False)
    feature_value_id = Column(
        Integer,
        ForeignKey(
            'feature_value.id'
        ),
        nullable=False
    )

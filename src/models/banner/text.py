from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText

from src.models.intl import IntlText


class BannerText(IntlText):
    __tablename__ = 'banner_text'

    value = Column(UnicodeText(), nullable=False)
    banner_id = Column(
        Integer,
        ForeignKey(
            'banner.id'
        ),
        nullable=False
    )

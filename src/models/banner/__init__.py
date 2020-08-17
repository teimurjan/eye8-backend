from sqlalchemy import Column, String, orm

from src.models.base import BaseModel


class Banner(BaseModel):
    __tablename__ = "banner"

    image = Column(String(255), nullable=False)
    texts = orm.relationship(
        "BannerText",
        backref="banner",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )
    link_texts = orm.relationship(
        "BannerLinkText",
        backref="banner",
        lazy="joined",
        cascade="all, delete, delete-orphan",
    )
    link = Column(String(255), nullable=True)
    text_color = Column(String(255), nullable=True)
    text_left_offset = Column(String(10), nullable=True)
    text_right_offset = Column(String(10), nullable=True)
    text_top_offset = Column(String(10), nullable=True)
    text_bottom_offset = Column(String(10), nullable=True)

    def __getitem__(self, key):
        if key == "texts":
            return self.texts
        if key == "link_texts":
            return self.link_texts

        return super().__getitem__(key)

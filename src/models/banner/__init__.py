from sqlalchemy import Column, String

from src.models.base import BaseModel


class Banner(BaseModel):
    __tablename__ = "banner"

    image = Column(String(255), nullable=False)
    text_en = Column(String(255), nullable=False)
    text_ru = Column(String(255), nullable=False)
    link_text_en = Column(String(255), nullable=False)
    link_text_ru = Column(String(255), nullable=False)
    link = Column(String(255), nullable=True)
    text_color = Column(String(255), nullable=True)
    text_left_offset = Column(String(10), nullable=True)
    text_right_offset = Column(String(10), nullable=True)
    text_top_offset = Column(String(10), nullable=True)
    text_bottom_offset = Column(String(10), nullable=True)

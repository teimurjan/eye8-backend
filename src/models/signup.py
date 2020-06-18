from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class Signup(BaseModel):
    __tablename__ = 'signup'

    user_name = Column(String(60), nullable=False)
    user_email = Column(String(80), unique=True, nullable=False)
    user_password = Column(String(250), nullable=False)

from typing import Any, cast
from sqlalchemy import Column, Integer, func, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = cast(Any, declarative_base())


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())


class NonDeletableModel(BaseModel):
    __abstract__ = True

    is_deleted = Column(Boolean, nullable=True, default=False)

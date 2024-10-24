from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Integer, Column, DateTime
from sqlalchemy.sql import func


@as_declarative()
class BaseModel:
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, index=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), onupdate=func.now())

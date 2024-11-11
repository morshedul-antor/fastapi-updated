from sqlalchemy import Column, String, Text, Integer, ForeignKey
from .base import BaseModel
from models import Base


class ToDo(Base, BaseModel):
    __tablename__ = "todos"

    title = Column(String(255))
    task = Column(Text, nullable=True)
    details = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

from sqlalchemy import Column, String
from models import BaseModel
from core import Base


class User(Base, BaseModel):
    __tablename__ = "users"

    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(30), nullable=True)
    password = Column(String(255), nullable=False)

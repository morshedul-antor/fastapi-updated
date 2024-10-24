from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class UserAuthOut(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

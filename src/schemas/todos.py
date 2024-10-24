from pydantic import BaseModel
from typing import Optional


class TodoBase(BaseModel):
    title: str
    task: Optional[str] = None
    details: Optional[str] = None


class TodoIn(TodoBase):
    user_id: Optional[int] = None


class TodoOut(TodoBase):
    user_id: int
    id: int

    class Config:
        from_attributes = True


class TodoOutUser(TodoBase):
    id: int

    class Config:
        from_attributes = True


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    task: Optional[str] = None
    details: Optional[str] = None

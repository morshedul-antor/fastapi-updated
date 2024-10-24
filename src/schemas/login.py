from pydantic import BaseModel


class LoginIn(BaseModel):
    identifier: str
    password: str


class LoginPasswordUpdate(BaseModel):
    password: str

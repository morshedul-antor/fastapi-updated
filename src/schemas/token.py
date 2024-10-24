from pydantic import BaseModel


class TokenDataIn(BaseModel):
    user_id: int


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class MessageOut(BaseModel):
    message: str

    class Config:
        from_attributes = True

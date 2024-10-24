from pydantic import BaseModel


class CountBase(BaseModel):
    counts: int


class CountOut(CountBase):
    pass

    class Config:
        from_attributes = True


class CountWithPaginationIn(CountBase):
    page: int
    skip: int
    limit: int


class CountWithPaginationOut(CountWithPaginationIn):
    pass

    class Config:
        from_attributes = True

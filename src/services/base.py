from exceptions import AppException, ServiceResult
from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session
from repositories import BaseRepo
from pydantic import BaseModel
from datetime import datetime
from fastapi import status
from models import Base

ModelType = TypeVar('ModelType', bound=Base)  # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelRepo = TypeVar("ModelRepo", bound=BaseRepo)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType], repo: Type[ModelRepo]):
        self.model = model
        self.repo = repo

    # ********** data create related methods ********** #
    def create(self, db: Session, data_in: CreateSchemaType):
        data = self.repo.create(db, data_in)
        if not data:
            return ServiceResult(AppException.ServerError("Something went wrong!"))

        return ServiceResult(data, status_code=status.HTTP_201_CREATED)

    def create_with_flush(self, db: Session, data_in: CreateSchemaType):
        data = self.repo.create_with_flush(db, data_in)
        if not data:
            return ServiceResult(AppException.ServerError("Something went wrong!"))

        return ServiceResult(data, status_code=status.HTTP_201_CREATED)

    # ********** data get related methods ********** #
    def get(self, db: Session):
        data = self.repo.get(db)
        if not data:
            return ServiceResult([], status_code=status.HTTP_200_OK)

        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_one(self, db: Session, id: int):
        data = self.repo.get_one(db, id)
        if not data:
            return ServiceResult(AppException.NotFound(f"No {self.model.__name__.lower}s found."))

        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_by_key_first(self, db: Session, **kwargs):
        data = self.repo.get_by_key_first(db=db, **kwargs)
        if not data:
            return ServiceResult(AppException.NotFound("Data not found!"))

        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_by_key(self, db: Session, count: bool = False, descending: bool = False, pagination: bool = False, page: int = None, skip: int = None, limit: int = 10, start_date: datetime = None,
                   end_date: datetime = None, **kwargs):
        data = self.repo.get_by_key(
            db=db, count=count, descending=descending, pagination=pagination, page=page, skip=skip, limit=limit, start_date=start_date, end_date=end_date, **kwargs
        )

        if not data:
            return ServiceResult([], status_code=status.HTTP_200_OK)

        return ServiceResult(data, status_code=status.HTTP_200_OK)

    # ********** data update related methods ********** #
    def update(self, db: Session, id: int, data_update: UpdateSchemaType):
        data = self.repo.update(db, id, data_update)
        if not data:
            return ServiceResult(AppException.NotAccepted())

        return ServiceResult(data, status_code=status.HTTP_202_ACCEPTED)

    def update_by_user_id(self, db: Session, user_id: int, data_update: UpdateSchemaType):
        data = self.repo.update_by_user_id(db, user_id, data_update)
        if not data:
            return ServiceResult(AppException.NotAccepted())

        return ServiceResult(data, status_code=status.HTTP_202_ACCEPTED)

    def update_after_check(self, db: Session, id: int, data_update: UpdateSchemaType, **kwargs):
        data = self.repo.get_by_key_first(db=db, id=id, **kwargs)

        if not data:
            return ServiceResult(AppException.NotFound("No data found!"))

        return self.update(db=db, id=id, data_update=data_update)

    # ********** data delete method ********** #
    def delete(self, db: Session, id: int):
        remove = self.repo.delete(db, id)
        if not remove:
            return ServiceResult(AppException.Forbidden())

        return ServiceResult(f"{id} successfully deleted", status_code=status.HTTP_202_ACCEPTED)

from typing import Generic, Optional, Type, TypeVar, Union, Dict, List, Any
from sqlalchemy.orm import Session
from .base_abstract import ABSRepo
from datetime import datetime
from models import BaseModel
from sqlalchemy import desc
from utils import Count
from core import Base

ModelType = TypeVar('ModelType', bound=Base)  # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepo(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABSRepo):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # ********** data create related methods ********** #
    def create(self, db: Session, data_in: CreateSchemaType) -> ModelType:
        data = self.model(**data_in.dict())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    def create_with_flush(self, db: Session, data_in: CreateSchemaType) -> ModelType:
        data = self.model(**data_in.dict())
        db.add(data)
        db.flush()
        return data

    def create_commit_with_refresh(self, db: Session, data_obj: ModelType) -> ModelType:
        db.commit()
        db.refresh(data_obj)
        return data_obj

    # ********** data get related methods ********** #
    def get(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def get_one(self, db: Session, id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()

    def filter_by_kwargs(self, db: Session, **kwargs) -> Any:
        query = db.query(self.model)

        for key, value in kwargs.items():
            if 'like' in key:
                query = query.filter(
                    getattr(self.model, key.split('_like')[0]).like(f"%{value}%"))
            else:
                query = query.filter(getattr(self.model, key) == value)

        return query

    def get_by_key_first(self, db: Session, **kwargs) -> Optional[ModelType]:
        return self.filter_by_kwargs(db, **kwargs).first()

    def get_by_key(self, db: Session, count: bool = False, descending: bool = False, pagination: bool = False, page: int = None, skip: int = None, limit: int = 10, start_date: datetime = None,
                   end_date: datetime = None, **kwargs) -> Union[List[ModelType], Dict[str, Any]]:
        query = self.filter_by_kwargs(db, **kwargs)

        if start_date and end_date:
            query = query.filter(
                self.model.created_at.between(start_date, end_date)
            )

        data_count = query.count() if count or pagination else None

        if descending:
            query = query.order_by(desc(self.model.created_at))

        if pagination:
            pagination_count = Count.pagination_count(
                page=page or 1, skip=skip or 0, limit=limit, count=data_count
            )
            query = query.offset(pagination_count.skip).limit(limit)

        data = query.all()

        if count and pagination:
            return [pagination_count, data]
        elif count:
            return [{"counts": data_count}, data]

        return data

    # ********** data update related methods ********** #
    def update(self, db: Session, id: int,  data_update: UpdateSchemaType) -> ModelType:
        db.query(self.model).filter(self.model.id == id).update(
            data_update.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return self.get_one(db, id)

    def update_by_user_id(self, db: Session, user_id: int,  data_update: UpdateSchemaType) -> ModelType:
        db.query(self.model).filter(self.model.user_id == user_id).update(
            data_update.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return self.get_by_key_first(db, user_id)

    # ********** data delete method ********** #
    def delete(self, db: Session, id: int) -> Optional[Union[ModelType, Any]]:
        result = db.query(self.model).filter(self.model.id ==
                                             id).delete(synchronize_session=False)
        db.commit()
        return result

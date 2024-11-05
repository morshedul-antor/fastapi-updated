from typing import Type, TypeVar, Optional, Union, Dict, List, Any
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from models import BaseModel
from core import Base

ModelType = TypeVar('ModelType', bound=Base)  # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ABSRepo(ABC):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    @abstractmethod
    def create(self, db: Session, data_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    def create_with_flush(self, db: Session, data_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    def create_commit_with_refresh(self, db: Session, data_obj: ModelType) -> ModelType:
        pass

    @abstractmethod
    def get(self, db: Session) -> List[ModelType]:
        pass

    @abstractmethod
    def get_one(self, db: Session, id: int) -> ModelType:
        pass

    @abstractmethod
    def get_by_key_first(self, db: Session, **kwargs) -> Optional[ModelType]:
        pass

    @abstractmethod
    def get_by_key(self, db: Session, count: bool, descending: bool, pagination: bool, page: int, skip: int, limit: int, **kwargs) -> Union[List[ModelType], Dict[str, Any]]:
        pass

    @abstractmethod
    def update(self, db: Session, id: int, data_update: UpdateSchemaType) -> ModelType:
        pass

    @abstractmethod
    def update_by_user_id(self, db: Session, user_id: int, data_update: UpdateSchemaType) -> ModelType:
        pass

    @abstractmethod
    def delete(self, db: Session, id: int) -> Optional[Union[ModelType, Any]]:
        pass

from exceptions import ServiceResult, AppException
from schemas import UserIn, UserUpdate
from sqlalchemy.orm import Session
from repositories import user_repo
from services import BaseService
from fastapi import status
from models import User
from utils import Hash


class UserService(BaseService[User, UserIn, UserUpdate]):

    def create_user(self, db: Session, data_in: UserIn, flush: bool):
        # phone & email check
        if self.repo.search_by_phone(db, data_in.phone):
            return ServiceResult(AppException.BadRequest("Phone number already exists!"))
        if self.repo.search_by_email(db, data_in.email):
            return ServiceResult(AppException.BadRequest("Email already exists!"))

        data_obj = data_in.dict(exclude={"password"})
        password = Hash.create_hash(data_in.password)
        data_obj.update({"password": password})

        if not flush:
            data = self.repo.create(db, data_in=UserIn(**data_obj))
        else:
            data = self.repo.create_with_flush(db, data_in=UserIn)

        if not data:
            return ServiceResult(AppException.ServerError("Something went wrong!"))

        return ServiceResult(data, status_code=status.HTTP_201_CREATED)


user_service = UserService(User, user_repo)

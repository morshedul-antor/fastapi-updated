from schemas import TodoIn, TodoUpdate
from sqlalchemy.orm import Session
from repositories import BaseRepo
from models import ToDo


class TodoRepo(BaseRepo[ToDo, TodoIn, TodoUpdate]):

    def create_todo(self, db: Session, data_in: TodoIn, user_id: int):
        data_for_db = TodoIn(user_id=user_id, **data_in.dict())
        todo = self.create(db=db, data_in=data_for_db)
        return todo


todo_repo = TodoRepo(ToDo)

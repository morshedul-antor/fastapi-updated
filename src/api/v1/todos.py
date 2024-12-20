from schemas import TodoBase, TodoOut, TodoOutUser, TodoUpdate, CountOut, CountWithPaginationOut
from fastapi import APIRouter, Depends
from exceptions import handle_result
from sqlalchemy.orm import Session
from services import todo_service
from typing import List, Union
from middlewares import Auth
from core import get_db

router = APIRouter()


@router.get('/', response_model=List[Union[CountWithPaginationOut, List[TodoOut]]])
def all_todo(page: int = 1, limit: int = 10, db: Session = Depends(get_db), current_user: Session = Depends(Auth.logged_in)):
    all = todo_service.get_by_key(
        db=db, count=True, descending=True, pagination=True, page=page, limit=limit)
    return handle_result(all)


@router.post('/', response_model=TodoOut)
def create_todo(data_in: TodoBase, db: Session = Depends(get_db), current_user: Session = Depends(Auth.logged_in)):
    todo = todo_service.create_todo(
        db=db, data_in=data_in, user_id=current_user.id)
    return handle_result(todo)


@router.get('/user-todo/', response_model=List[Union[CountOut, List[TodoOutUser]]])
def user_todo(skip: int = 0, limit: int = 10,  db: Session = Depends(get_db), current_user: Session = Depends(Auth.logged_in)):
    user_id = current_user.id
    all = todo_service.get_by_key(
        db=db, count=True, descending=True, pagination=True, skip=skip, limit=limit, user_id=user_id)
    return handle_result(all)


@router.get('/{id}', response_model=TodoOut)
def get_one(id, db: Session = Depends(get_db), current_user: Session = Depends(Auth.logged_in)):
    todo = todo_service.get_one(db, id)
    return handle_result(todo)


@router.put('/{id}', response_model=TodoOut)
def update_todo(id: int, todo_update: TodoUpdate, db: Session = Depends(get_db), current_user: Session = Depends(Auth.logged_in)):
    update = todo_service.update(db, id, data_update=todo_update)
    return handle_result(update)


@router.delete('/{id}')
def delete_todo(id: int, db: Session = Depends(get_db), current_user: Session = Depends(Auth.logged_in)):
    delete = todo_service.delete(db, id=id)
    return handle_result(delete)

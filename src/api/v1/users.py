from schemas import UserIn, UserOut, UserAuthOut, UserUpdate, CountWithPaginationOut, CountOut
from fastapi import APIRouter, Depends
from exceptions import handle_result
from sqlalchemy.orm import Session
from services import user_service
from typing import List, Union
from middlewares import Auth
from core import get_db

router = APIRouter()


@router.get('/', response_model=List[Union[CountOut, List[UserOut]]])
def all_user(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    data = user_service.get_by_key(
        db=db, count=True, descending=True, start_date=start_date, end_date=end_date)
    return handle_result(data)


@router.post('/', response_model=UserOut)
def create_user(data_in: UserIn, db: Session = Depends(get_db)):
    user = user_service.create_user(db=db, data_in=data_in, flush=False)
    return handle_result(user)


@router.get('/{id}', response_model=UserAuthOut)
def get_one(id, db: Session = Depends(get_db), current_user: Session = Depends(Auth.logged_in)):
    todo = user_service.get_one(db, id)
    return handle_result(todo)


@router.put('/{id}', response_model=UserOut)
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: Session = Depends(Auth.logged_in)):
    update = user_service.update(db, id, data_update=user_update)
    return handle_result(update)

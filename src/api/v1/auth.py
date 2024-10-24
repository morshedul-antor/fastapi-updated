from schemas import LoginIn, TokenOut, UserAuthOut
from fastapi import APIRouter, Depends
from exceptions import handle_result
from sqlalchemy.orm import Session
from services import login_service
from middlewares import Auth
from models import User
from db import get_db

router = APIRouter()


@router.post('/login/')
def login(data_in: LoginIn, db: Session = Depends(get_db)):
    user = login_service.login(db, data_in.identifier, data_in.password)
    return handle_result(user)


@router.get('/auth/', response_model=UserAuthOut)
def auth(current_user: User = Depends(Auth.logged_in)):
    return current_user

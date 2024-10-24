from api.v1 import auth, users, todos
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(auth.router, prefix='', tags=['Auth'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(todos.router, prefix='/todo', tags=['Todos'])

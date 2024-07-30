from http import HTTPStatus

from fastapi import FastAPI

from curso_fast.routers import auth, todo, users
from curso_fast.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todo.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, world!'}

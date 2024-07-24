from http import HTTPStatus

from fastapi import FastAPI

from curso_fast.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, world!'}
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from curso_fast.database import get_session
from curso_fast.models import User
from curso_fast.schemas import (
    Token,
)
from curso_fast.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2_Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def login(
    session: T_Session,
    form_data: T_OAuth2_Form,
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid credentials'
        )

    access_token = create_access_token({'sub': user.email})

    return {
        'access_token': access_token,
        'token_type': 'Bearer',
    }

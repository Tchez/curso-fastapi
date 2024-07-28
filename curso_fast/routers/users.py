from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from curso_fast.database import get_session
from curso_fast.models import User
from curso_fast.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from curso_fast.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

T_Session = Annotated[Session, Depends(get_session)]
T_Current_User = Annotated[User, Depends(get_current_user)]


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: T_Session,
    limit: int = 10,
    offset: int = 0,
):
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(
    session: T_Session,
    user_id: int,
):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    session: T_Session,
    user: UserSchema,
):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already registered',
            )

    db_user = User(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    session: T_Session,
    current_user: T_Current_User,
    user_id: int,
    user: UserSchema,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    current_user.email = user.email
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    session: T_Session,
    current_user: T_Current_User,
    user_id: int,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}

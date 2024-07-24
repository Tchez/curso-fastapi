from sqlalchemy import select

from curso_fast.models import User


def test_create_user(session):
    user = User(
        username='teste',
        email='teste@mail.com',
        password='password',
    )

    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'teste@mail.com'))

    assert result.id == 1
    assert result.username == 'teste'
    assert result.email == 'teste@mail.com'
    assert result.password == 'password'

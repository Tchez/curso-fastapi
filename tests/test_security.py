from http import HTTPStatus

from jwt import decode

from curso_fast.security import create_access_token, settings


def test_jwt():
    data = {'sub': 'test@test.com'}

    token = create_access_token(data)
    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert result['sub'] == data['sub']
    assert 'exp' in result


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_invalid_user_payload(client):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6MTcyMjEwNTM5M30.j2FJjuzEKr75nKriVweI0AdOgGLYxXfsO2pYAyR-jrY'  # noqa
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

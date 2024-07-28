from http import HTTPStatus

from curso_fast.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'test_username',
            'password': 'pass',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test_username',
        'email': 'test@test.com',
    }


def test_create_user_com_username_ja_existente_deve_retornar_bad_request(
    client, user
):
    response = client.post(
        '/users',
        json={
            'username': 'Teste',
            'password': 'pass',
            'email': 'outro_mail@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_com_email_ja_existente_deve_retornar_bad_request(
    client, user
):
    response = client.post(
        '/users',
        json={
            'username': 'outro_username',
            'password': 'pass',
            'email': 'teste@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already registered'}


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_com_id_invalido_deve_retornar_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test_username_updated',
            'password': 'pass',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test_username_updated',
        'email': 'test@test.com',
    }


def test_update_user_com_id_invalido_deve_retornar_not_enough_permissions(
    client, user, token
):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test_username_updated',
            'password': 'pass',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_com_id_invalido_deve_retornar_not_enough_permissions(
    client, user, token
):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}

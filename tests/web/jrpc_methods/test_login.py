import sqlalchemy

from common import db


async def test_login_no_user(jrpc_client) -> None:
    response = await jrpc_client(
        method='login',
        params={
            'login_data': {
                'email': 'any@gmail.com',
                'password': 'sdfsdvjsodl',
            },
        },
    )
    assert response.failed
    assert response.error['code'] == -32003


async def test_incorrect_password(jrpc_client, user: db.User) -> None:
    response = await jrpc_client(
        method='login',
        params={
            'login_data': {
                'email': user.email,
                'password': 'sdfsdvjsodl',
            },
        },
    )
    assert response.failed
    assert response.error['code'] == -32003


async def test_correct_password_and_email(jrpc_client, user_with_pwd) -> None:
    response = await jrpc_client(
        method='login',
        params={'login_data': {'email': user_with_pwd.email, 'password': 'mafia'}},
    )
    assert response.success
    assert response.result is True

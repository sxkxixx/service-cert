import dirty_equals

from common import db


async def test_register_user(jrpc_client):
    method = 'register_user'
    params = {
        'data': {
            'first_name': 'Михаил',
            'last_name': 'Зюбенко',
            'email': 'zubenko.mikhail@gmail.com',
            'password': 'mafia',
        }
    }
    response = await jrpc_client(method=method, params=params)

    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'first_name': 'Михаил',
        'last_name': 'Зюбенко',
        'email': 'zubenko.mikhail@gmail.com',
    }


async def test_register_user_email_duplicate(jrpc_client, user: db.User):
    method = 'register_user'
    params = {
        'data': {
            'first_name': 'Михаил',
            'last_name': 'Зюбенко',
            'email': user.email,
            'password': 'mafia2',
        }
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32002
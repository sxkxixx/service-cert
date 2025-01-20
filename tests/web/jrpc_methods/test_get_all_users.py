import dirty_equals

from common import db

method = 'get_all_users'


async def test_get_all_users_empty(jrpc_client) -> None:
    response = await jrpc_client(method=method, params={})
    assert response.success
    assert response.result == []


async def test_get_all_users(jrpc_client, user: db.User) -> None:
    response = await jrpc_client(method=method, params={})
    assert response.success
    assert response.result == [
        {
            'id': dirty_equals.IsUUID(version=4),
            'name': user.name,
            'nickname': user.nickname,
            'email': user.email,
        }
    ]

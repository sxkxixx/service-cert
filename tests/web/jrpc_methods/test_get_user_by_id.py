import uuid

from common import db

method = 'get_user_by_id'


async def test_get_user_by_id_bot_found(jrpc_client) -> None:
    params = {'id': str(uuid.uuid4())}
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_get_user_by_id(jrpc_client, user: db.User) -> None:
    params = {'id': str(user.id)}
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': str(user.id),
        'name': user.name,
        'nickname': user.nickname,
        'email': user.email,
    }

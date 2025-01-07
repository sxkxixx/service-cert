import uuid

from common.jwt import AccessToken

method = 'delete_user'


async def test_delete_user_unauthorized(jrpc_client) -> None:
    response = await jrpc_client(method=method, params={})
    assert response.failed
    assert response.error['code'] == -32003


async def test_delete_user_ok(authorized_jrpc_client) -> None:
    response = await authorized_jrpc_client(method=method, params={})
    assert response.success


async def test_delete_not_exists_user(jrpc_client) -> None:
    payload = {'id': str(uuid.uuid4())}
    access_token = AccessToken(payload=payload)
    response = await jrpc_client(
        method=method, params={}, headers={'Authorization': access_token.encode()}
    )
    assert response.failed
    assert response.error['code'] == -32003

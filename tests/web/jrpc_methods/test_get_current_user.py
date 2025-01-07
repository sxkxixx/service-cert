method = 'get_current_user'


async def test_get_current_user_ok(authorized_jrpc_client, user) -> None:
    response = await authorized_jrpc_client(method=method, params={})
    assert response.result == {
        'id': str(user.id),
        'name': user.name,
        'nickname': user.nickname,
        'email': user.email,
    }


async def test_get_current_user_unauthorized(jrpc_client) -> None:
    response = await jrpc_client(method=method, params={})
    assert response.failed
    assert response.error['code'] == -32003

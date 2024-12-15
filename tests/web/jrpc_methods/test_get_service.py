import uuid


async def test_get_service_not_found(jrpc_client) -> None:
    params = {'service_id': str(uuid.uuid4())}
    response = await jrpc_client(method='get_service', params=params)

    assert response.failed
    assert response.error['code'] == -32001

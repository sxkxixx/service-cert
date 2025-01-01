async def test_create_service(jrpc_client) -> None:
    params = {'service': {'name': 'Сервис аттестации релизов', 'description': '120-3912-912321'}}
    response = await jrpc_client(method='create_service', params=params)
    assert response.success


async def test_create_service_null_description(jrpc_client) -> None:
    params = {'service': {'name': 'Сервис аттестации релизов', 'description': None}}
    response = await jrpc_client(method='create_service', params=params)
    assert response.success

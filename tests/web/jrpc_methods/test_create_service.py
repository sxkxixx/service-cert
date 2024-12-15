async def test_create_service(jrpc_client):
    params = {'service': {'name': 'Сервис аттестации релизов', 'description': '120-3912-912321'}}
    response = await jrpc_client(method='create_service', params=params)
    assert response.success

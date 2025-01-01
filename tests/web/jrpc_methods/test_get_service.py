import uuid

from common import db


async def test_get_service_not_found(jrpc_client) -> None:
    params = {'service_id': str(uuid.uuid4())}
    response = await jrpc_client(method='get_service', params=params)

    assert response.failed
    assert response.error['code'] == -32001


async def test_get_service(service: db.Service, jrpc_client) -> None:
    params = {'service_id': str(service.id)}
    response = await jrpc_client(method='get_service', params=params)

    assert response.success
    assert response.result == {
        'name': service.name,
        'description': service.description,
        'id': str(service.id),
        'confluence_page_link': None,
        'requirements': [],
    }

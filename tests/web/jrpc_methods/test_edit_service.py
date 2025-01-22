import uuid

from common import db

method = 'edit_service'


async def test_edit_service_service_not_found(
    jrpc_client,
) -> None:
    params = {
        'service_id': str(uuid.uuid4()),
        'name': 'Сервис аттестации релизов',
        'description': 'Описание сервиса аттестации релизов',
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_edit_service_ok(
    jrpc_client,
    service: db.Service,
) -> None:
    params = {
        'service_id': str(service.id),
        'name': 'Сервис аттестации релизов',
        'description': 'Описание сервиса аттестации релизов',
    }
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': str(service.id),
        'name': 'Сервис аттестации релизов',
        'description': 'Описание сервиса аттестации релизов',
        'confluence_page_link': service.confluence_page_link,
    }

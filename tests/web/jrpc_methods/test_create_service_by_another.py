import uuid

import dirty_equals

from common import db

method = 'create_service_by_another'


async def test_create_service_ok(
    jrpc_client,
    service_with_requirement: db.Service,
) -> None:
    params = {
        'service': {
            'name': 'Сервис по шаблону',
            'description': None,
            'source_service_id': str(service_with_requirement.id),
        }
    }
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'name': 'Сервис по шаблону',
        'description': None,
        'confluence_page_link': None,
        'requirements': [
            {
                'name': 'Требование сервиса',
                'value': None,
                'id': dirty_equals.IsUUID(version=4),
                'responsible_id': None,
            }
        ],
    }


async def test_source_service_not_found(jrpc_client) -> None:
    params = {
        'service': {
            'name': 'Сервис по шаблону',
            'description': None,
            'source_service_id': str(uuid.uuid4()),
        }
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001

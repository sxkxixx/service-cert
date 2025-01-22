import uuid

import dirty_equals

from common import db

method = 'create_release_arbitrarily'


async def test_create_release_arbitrarily_ok(
    jrpc_client,
    service: db.Service,
) -> None:
    params = {
        'service_id': str(service.id),
        'name': 'Релиз 1',
        'semantic_version': 'v0.0.1',
        'requirements': [
            {'name': 'smth', 'value': None},
        ],
    }
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'service_id': str(service.id),
        'name': 'Релиз 1',
        'semantic_version': 'v0.0.1',
        'requirements': [
            {
                'id': dirty_equals.IsUUID(version=4),
                'name': 'smth',
                'value': None,
                'responsible_id': None,
                'type': None,
            },
        ],
    }


async def test_service_not_found(jrpc_client) -> None:
    params = {
        'service_id': str(uuid.uuid4()),
        'name': 'Релиз 1',
        'semantic_version': 'v0.0.1',
        'requirements': [
            {'name': 'smth', 'value': None},
        ],
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001

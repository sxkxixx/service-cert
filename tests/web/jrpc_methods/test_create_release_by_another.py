import uuid

import dirty_equals

from common import db

method = 'create_release_by_another'


async def test_service_not_found(
    jrpc_client,
) -> None:
    params = {
        'release': {
            'name': 'abcdef',
            'service_id': str(uuid.uuid4()),
            'semantic_version': None,
            'source_release_id': str(uuid.uuid4()),
        },
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_release_not_found(
    jrpc_client,
    service: db.Service,
) -> None:
    params = {
        'release': {
            'name': 'abcdef',
            'service_id': str(service.id),
            'semantic_version': None,
            'source_release_id': str(uuid.uuid4()),
        },
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_create_by_release_without_requirements(
    jrpc_client,
    release: db.Release,
) -> None:
    params = {
        'release': {
            'name': 'abcdef',
            'service_id': str(release.service_id),
            'semantic_version': 'v0.0.1',
            'source_release_id': str(release.id),
        },
    }
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'service_id': str(release.service_id),
        'description': None,
        'name': 'abcdef',
        'semantic_version': 'v0.0.1',
        'requirements': [],
    }


async def test_create_by_another_ok(
    jrpc_client,
    release_with_requirements: db.Release,
) -> None:
    params = {
        'release': {
            'name': 'abcdef',
            'description': 'description',
            'service_id': str(release_with_requirements.service_id),
            'semantic_version': 'v0.0.1',
            'source_release_id': str(release_with_requirements.id),
        },
    }
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'service_id': str(release_with_requirements.service_id),
        'name': 'abcdef',
        'semantic_version': 'v0.0.1',
        'description': 'description',
        'requirements': [
            {
                'id': dirty_equals.IsUUID(version=4),
                'name': 'Требование релиза',
                'value': None,
                'responsible_id': None,
                'type': None,
            }
        ],
    }

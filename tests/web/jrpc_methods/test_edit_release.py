import uuid

from common import db

method = 'edit_release'


async def test_edit_release_not_found_release(
    jrpc_client,
) -> None:
    params = {
        'release_id': str(uuid.uuid4()),
        'name': 'Сервис аттестации релизов',
        'description': 'Описание сервиса аттестации релизов',
        'semantic_version': None,
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_edit_release_ok(jrpc_client, release: db.Release) -> None:
    params = {
        'release_id': str(release.id),
        'name': 'Сервис аттестации релизов',
        'description': 'Описание сервиса аттестации релизов',
        'semantic_version': None,
    }
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': str(release.id),
        'service_id': str(release.service_id),
        'name': 'Сервис аттестации релизов',
        'semantic_version': None,
        'description': 'Описание сервиса аттестации релизов',
    }

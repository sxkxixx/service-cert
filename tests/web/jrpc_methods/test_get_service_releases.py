import uuid

from common import db

method = 'get_service_releases'


async def test_no_service_by_id(jrpc_client) -> None:
    response = await jrpc_client(method=method, params={'service_id': str(uuid.uuid4())})
    assert response.success
    assert response.result == []


async def test_service_without_releases(jrpc_client, service: db.Service) -> None:
    response = await jrpc_client(method=method, params={'service_id': str(service.id)})
    assert response.success
    assert response.result == []


async def test_service_with_release(jrpc_client, release: db.Release) -> None:
    response = await jrpc_client(method=method, params={'service_id': str(release.service_id)})
    assert response.success
    assert response.result == [
        {
            'id': str(release.id),
            'service_id': str(release.service_id),
            'name': release.name,
            'semantic_version': release.semantic_version,
            'description': release.description,
        }
    ]

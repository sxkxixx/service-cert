import uuid

from common import db


async def test_search_release_with_nullable_name(
    release: db.Release,
    jrpc_client,
) -> None:
    params = {
        'name': None,
        'batch': {
            'limit': 10,
            'offset': 0,
        },
    }
    response = await jrpc_client(
        method='search_releases',
        params=params,
    )
    assert response.success
    assert response.result == [
        {
            'id': str(release.id),
            'service_id': str(release.service_id),
            'name': str(release.name),
            'semantic_version': release.semantic_version,
        }
    ]


async def test_no_releases_by_name(
    release: db.Release,
    jrpc_client,
) -> None:
    params = {
        'name': str(uuid.uuid4()),
        'batch': {
            'limit': 10,
            'offset': 0,
        },
    }
    response = await jrpc_client(
        method='search_releases',
        params=params,
    )
    assert response.success
    assert response.result == []

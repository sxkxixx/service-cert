import uuid

import dirty_equals

from common import db

method = 'get_release'


async def test_get_release_not_found(jrpc_client) -> None:
    response = await jrpc_client(method=method, params={'release_id': str(uuid.uuid4())})
    assert response.failed
    assert response.error['code'] == -32001


async def test_get_release_no_requirements(
    jrpc_client,
    release: db.Release,
) -> None:
    response = await jrpc_client(method=method, params={'release_id': str(release.id)})
    assert response.success
    assert response.result == {
        'id': str(release.id),
        'service_id': str(release.service_id),
        'name': release.name,
        'semantic_version': release.semantic_version,
        'description': release.description,
        'requirements': [],
        'release_page': None,
    }


async def test_get_release_with_requirements(
    jrpc_client,
    release_with_requirements: db.Release,
    release_page: db.ReleasePage,
) -> None:
    response = await jrpc_client(
        method=method, params={'release_id': str(release_with_requirements.id)}
    )
    assert response.success
    assert response.result == {
        'id': str(release_with_requirements.id),
        'service_id': str(release_with_requirements.service_id),
        'name': release_with_requirements.name,
        'semantic_version': release_with_requirements.semantic_version,
        'description': release_with_requirements.description,
        'requirements': [
            {
                'id': dirty_equals.IsUUID(version=4),
                'name': 'Требование релиза',
                'value': 'Значение требования релиза',
                'type': None,
                'responsible_id': None,
            }
        ],
        'release_page': {
            'page_id': release_page.page_id,
            'release_id': str(release_page.release_id),
            'service_space_id': str(release_page.service_space_id),
            'webui_link': '',
        },
    }

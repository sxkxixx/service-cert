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
        'team': [],
        'service_space': None,
    }


async def test_get_service_with_space(
    jrpc_client,
    service_need_create_release_folder: db.Service,
    service_space: db.ServiceSpace,
) -> None:
    params = {'service_id': str(service_need_create_release_folder.id)}
    response = await jrpc_client(method='get_service', params=params)
    assert response.success
    assert response.result == {
        'name': service_need_create_release_folder.name,
        'description': service_need_create_release_folder.description,
        'id': str(service_need_create_release_folder.id),
        'confluence_page_link': None,
        'requirements': [],
        'team': [],
        'service_space': {
            'id': str(service_space.id),
            'service_id': str(service_space.service_id),
            'webui_link': service_space.webui_link,
            'homepage_id': service_space.homepage_id,
            'release_folder_id': service_space.release_folder_id,
            'ext_id': service_space.ext_id,
            'key': service_space.key,
            'alias': service_space.alias,
        },
    }

from common import db


async def test_get_services(
    jrpc_client,
    service: db.Service,
) -> None:
    response = await jrpc_client(
        method='get_services', params={'batch': {'offset': 0, 'limit': 1}}
    )
    assert response.success

    assert response.result == [{
        'id': str(service.id),
        'name': service.name,
        'description': service.description,
        'confluence_page_link': service.confluence_page_link,
    }]


async def test_offset_more_than_total_count(
    jrpc_client,
    service: db.Service,
) -> None:
    response = await jrpc_client(
        method='get_services', params={'batch': {'offset': 2, 'limit': 1}}
    )
    assert response.success
    assert response.result == []

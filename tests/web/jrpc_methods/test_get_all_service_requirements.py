import dirty_equals

from common import db

method = 'get_all_service_requirements'
params = {'batch': {'limit': 50, 'offset': 0}}


async def test_get_all_service_requirements_empty(jrpc_client) -> None:
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == []


async def test_get_all_rr_not_empty(
    jrpc_client, service_requirement: db.ServiceRequirement
) -> None:
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == [
        {'id': dirty_equals.IsUUID(version=4), 'name': service_requirement.name}
    ]

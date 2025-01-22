import uuid

from common import db

method = 'edit_service_requirement'


async def test_not_found(jrpc_client) -> None:
    params = {
        'requirement_id': str(uuid.uuid4()),
        'name': 'Gitlab',
        'value': None,
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_edit_ok(jrpc_client, service_requirement: db.ServiceRequirement) -> None:
    params = {
        'requirement_id': str(service_requirement.id),
        'name': 'Gitlab',
        'value': None,
    }
    response = await jrpc_client(method=method, params=params)
    assert response.result == {
        'id': str(service_requirement.id),
        'name': 'Gitlab',
        'value': None,
        'type': None,
        'responsible_id': None,
    }

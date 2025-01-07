import uuid

import dirty_equals

from common import db

method = 'add_service_requirement'


async def test_service_not_found(authorized_jrpc_client) -> None:
    params = {'service_id': str(uuid.uuid4()), 'requirement': {'name': 'abcdef', 'value': None}}
    response = await authorized_jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_create_service_requirement_ok(
    authorized_jrpc_client,
    user: db.User,
    service: db.Service,
) -> None:
    params = {'service_id': str(service.id), 'requirement': {'name': 'abcdef', 'value': None}}
    response = await authorized_jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'name': 'abcdef',
        'value': None,
        'responsible_id': str(user.id),
    }

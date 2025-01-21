import uuid

import dirty_equals

from common import db

method = 'edit_service_team'


async def test_edit_service_team_service_not_found(
    jrpc_client,
) -> None:
    params = {'service_id': str(uuid.uuid4()), 'teammates_ids': [str(uuid.uuid4())]}
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_edit_service_team_ok(
    jrpc_client,
    user: db.User,
    service: db.Service,
) -> None:
    params = {'service_id': str(service.id), 'teammates_ids': [str(user.id)]}
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == [
        {
            'id': dirty_equals.IsUUID(version=4),
            'user_id': str(user.id),
        }
    ]

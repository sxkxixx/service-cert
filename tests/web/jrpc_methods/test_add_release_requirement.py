import uuid

import dirty_equals

from common import db

method = 'add_release_requirement'


async def test_add_release_requirement_release_not_found(
    authorized_jrpc_client,
) -> None:
    params = {'release_id': str(uuid.uuid4()), 'requirement': {'name': 'abcdef', 'value': None}}
    response = await authorized_jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_add_release_requirement_ok(
    authorized_jrpc_client,
    user: db.User,
    release: db.Release,
) -> None:
    params = {'release_id': str(release.id), 'requirement': {'name': 'abcdef', 'value': None}}
    response = await authorized_jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'name': 'abcdef',
        'value': None,
        'responsible_id': str(user.id),
    }

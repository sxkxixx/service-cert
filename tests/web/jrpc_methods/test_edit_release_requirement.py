import uuid

from common import db

method = 'edit_release_requirement'


async def test_not_found(jrpc_client) -> None:
    params = {
        'requirement_id': str(uuid.uuid4()),
        'name': 'Gitlab',
        'value': None,
    }
    response = await jrpc_client(method=method, params=params)
    assert response.failed
    assert response.error['code'] == -32001


async def test_edit_ok(jrpc_client, release_requirement: db.ReleaseRequirement) -> None:
    params = {
        'requirement_id': str(release_requirement.id),
        'name': 'Gitlab',
        'value': None,
    }
    response = await jrpc_client(method=method, params=params)
    assert response.result == {
        'id': str(release_requirement.id),
        'name': 'Gitlab',
        'value': None,
    }

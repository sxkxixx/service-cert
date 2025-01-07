import uuid

from common import db

method = 'delete_service_requirement'


async def test_requirement_not_found(jrpc_client) -> None:
    response = await jrpc_client(method=method, params={'requirement_id': str(uuid.uuid4())})
    assert response.failed
    assert response.error['code'] == -32001


async def test_delete_ok(jrpc_client, service_requirement: db.ReleaseRequirement) -> None:
    response = await jrpc_client(
        method=method, params={'requirement_id': str(service_requirement.id)}
    )
    assert response.success

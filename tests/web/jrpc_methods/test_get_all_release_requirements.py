from common import db

method = 'get_all_release_requirements'
params = {'batch': {'limit': 50, 'offset': 0}}


async def test_get_all_release_requirements_empty(jrpc_client) -> None:
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == []


async def test_get_all_rr_not_empty(
    jrpc_client, release_requirement: db.ReleaseRequirement
) -> None:
    response = await jrpc_client(method=method, params=params)
    assert response.success
    assert response.result == [release_requirement.name]

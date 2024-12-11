import pytest

from common import db


@pytest.mark.parametrize('offset, limit', [(-10, -10), (10, -10), (-10, 10)])
async def test_negative_batch_params(
    jrpc_client,
    offset: int,
    limit: int,
) -> None:
    response = await jrpc_client(
        method='get_template_list', params={'batch': {'offset': offset, 'limit': limit}}
    )
    assert response.failed
    assert response.error['code'] == -32602


async def test_positive_limit_zero_offset(
    jrpc_client,
    template: db.Template,
) -> None:
    response = await jrpc_client(
        method='get_template_list', params={'batch': {'offset': 0, 'limit': 1}}
    )
    assert response.success
    result = response.result

    assert result == [
        {
            'id': str(template.id),
            'name': template.name,
            'requirements': [],
        },
    ]


async def test_offset_more_than_total_count(
    jrpc_client,
    template: db.Template,
) -> None:
    response = await jrpc_client(
        method='get_template_list', params={'batch': {'offset': 2, 'limit': 1}}
    )
    assert response.success
    assert response.result == []

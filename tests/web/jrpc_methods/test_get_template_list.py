import pytest
import sqlalchemy

from common import db


@pytest.mark.parametrize('offset, limit', [(-10, -10), (10, -10), (-10, 10)])
async def test_negative_batch_params(
    jrpc_client,
    offset: int,
    limit: int,
) -> None:
    response = await jrpc_client(method='get_template_list', params={'batch': {'offset': offset, 'limit': limit}})
    assert response.failed
    assert response.error['code'] == -32602


@pytest.fixture(scope='function')
async def template(db_session) -> db.Template:
    template = await db_session.scalar(
        sqlalchemy.insert(db.Template)
        .values(name='Шаблон 1')
        .returning(db.Template)
    )
    await db_session.commit()
    return template


async def test_positive_limit_zero_offset(
    jrpc_client,
    template: db.Template,
) -> None:
    response = await jrpc_client(method='get_template_list', params={'batch': {'offset': 0, 'limit': 1}})
    assert response.success
    result = response.result

    assert result == {
        'id': template.id,
        'name': 'Шаблон 1',
        'requirements': [],
    }

import os
import uuid
from unittest import mock

import pytest
import sqlalchemy

from common import db, enums
from common.schemas.space import ConfluenceSpaceResponse
from jobs import background_tasks


async def _get_service(service_id: uuid.UUID) -> db.Service | None:
    async with db.AsyncSession() as session:
        return await session.scalar(
            sqlalchemy.select(db.Service).where(db.Service.id == service_id)
        )


async def get_service_space(service_id: uuid.UUID) -> db.ServiceSpace | None:
    async with db.AsyncSession() as session:
        return await session.scalar(
            sqlalchemy.select(db.ServiceSpace).where(db.ServiceSpace.service_id == service_id)
        )


@pytest.fixture()
async def mock_create_space(service_space_generating: db.Service) -> None:
    with mock.patch(
        'common.confluence.space.create_service_space',
        return_value=ConfluenceSpaceResponse(
            id=987654321,
            key='f9d3bee527d91ccc5f057da4e83b7667',
            alias='f9d3bee527d91ccc5f057da4e83b7667',
            name=service_space_generating.name,
            homepage={'id': 1234567890},
            _links={
                'base': 'https://confluence.net',
                'webui': '/spaces/f9d3bee527d91ccc5f057da4e83b7667',
            },
        ),
    ) as mock_create_service_space:
        yield mock_create_service_space


async def test(
    service_space_generating: db.Service,
    mock_create_space: mock.Mock,
) -> None:
    await background_tasks.generate_space.generate_space()

    service = await _get_service(service_id=service_space_generating.id)
    assert service.status == enums.ServiceStatus.NEED_CREATE_RELEASE_FOLDER

    service_space = await get_service_space(service_id=service.id)
    assert service_space.key == service_space.alias
    assert (
        service_space.webui_link == 'https://confluence.net/spaces/f9d3bee527d91ccc5f057da4e83b7667'
    )
    assert service_space.ext_id == 987654321

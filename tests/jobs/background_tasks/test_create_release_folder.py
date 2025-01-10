import uuid
from unittest import mock

import pytest
import sqlalchemy

from common import db, enums
from jobs import background_tasks


@pytest.fixture
def mock_create_folder() -> mock.Mock:
    with mock.patch('common.confluence.folder.create_folder') as mock_:
        yield mock_


async def _get_service(service_id: uuid.UUID) -> db.Service | None:
    async with db.AsyncSession() as session:
        return await session.scalar(
            sqlalchemy.select(db.Service)
            .where(db.Service.id == service_id)
        )


async def get_service_space(service_id: uuid.UUID) -> db.ServiceSpace | None:
    async with db.AsyncSession() as session:
        return await session.scalar(
            sqlalchemy.select(db.ServiceSpace).where(db.ServiceSpace.service_id == service_id)
        )


async def test_create_release_folder_ok(
    service_need_create_release_folder: db.Service,
    service_space: db.ServiceSpace,
) -> None:
    await background_tasks.generate_release_folder.create_release_folder()

    service = await _get_service(service_id=service_need_create_release_folder.id)
    assert service.status == enums.ServiceStatus.NEED_UPDATE_HOMEPAGE

    service_page = await get_service_space(service_id=service.id)
    assert service_page.release_folder_id == ''

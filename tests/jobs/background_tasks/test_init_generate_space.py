import uuid

import sqlalchemy

from common import db, enums
from jobs import background_tasks


async def _get_service(service_id: uuid.UUID) -> db.Service | None:
    async with db.AsyncSession() as session:
        return await session.scalar(
            sqlalchemy.select(db.Service).where(db.Service.id == service_id)
        )


async def test_init_generate_space_ok(service: db.Service) -> None:
    await background_tasks.generate_pages.init_generate_space()
    service = await _get_service(service_id=service.id)
    assert service.status == enums.ServiceStatus.GENERATING_CONFLUENCE_SPACE

import uuid

import sqlalchemy
from sqlalchemy.orm import selectinload

from common import db


async def get_services(offset: int, limit: int) -> list[db.Service]:
    async with db.AsyncSession() as session:
        stmt = (
            sqlalchemy.select(db.Service)
            # .options(selectinload(db.Service.releases))
            .offset(offset=offset)
            .limit(limit=limit)
        )
        result = await session.execute(stmt)
    return result.scalars().all()


async def get_service(service_id: uuid.UUID) -> db.Service | None:
    query = (
        sqlalchemy.select(db.Service)
        .filter(db.Service.id == service_id)
        .options(selectinload(db.Service.service_requirements))
    )

    async with db.AsyncSession() as session:
        service = await session.scalar(statement=query)
    return service

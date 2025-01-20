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


async def get_service_with_requirements(service_id: uuid.UUID) -> db.Service | None:
    query = (
        sqlalchemy.select(db.Service)
        .filter(db.Service.id == service_id)
        .options(selectinload(db.Service.service_requirements))
    )

    async with db.AsyncSession() as session:
        service = await session.scalar(statement=query)
    return service


def get_service_stmt(service_id: uuid.UUID, lock: bool = False) -> sqlalchemy.Select:
    query = sqlalchemy.select(db.Service).where(db.Service.id == service_id)
    if lock:
        return query.with_for_update()
    return query


async def get_services_by_name(name: str) -> list[db.Service]:
    statement = sqlalchemy.select(db.Service).where(db.Service.name.like(name))
    async with db.AsyncSession() as session:
        return await session.scalars(statement=statement)

import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from common import db, enums


async def get_services(offset: int, limit: int) -> list[db.Service]:
    async with db.AsyncSession() as session:
        stmt = sqlalchemy.select(db.Service).offset(offset=offset).limit(limit=limit)
        result = await session.execute(stmt)
    return result.scalars().all()


async def get_service_with_requirements(service_id: uuid.UUID) -> db.Service | None:
    query = (
        sqlalchemy.select(db.Service)
        .filter(db.Service.id == service_id)
        .options(
            selectinload(db.Service.service_requirements),
            selectinload(db.Service.team),
        )
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


async def get_service_for_generate_space(
    session: AsyncSession,
    lock: bool = False,
) -> db.Service | None:
    statement = (
        sqlalchemy.select(db.Service).where(db.Service.status == enums.ServiceStatus.NEW).limit(1)
    )
    if lock:
        statement = statement.with_for_update()
    return await session.scalar(statement)


async def get_service_ready_to_generate_space(session: AsyncSession) -> db.Service | None:
    statement = (
        sqlalchemy.select(db.Service)
        .where(db.Service.status == enums.ServiceStatus.GENERATING_CONFLUENCE_SPACE)
        .limit(1)
    )
    return await session.scalar(statement=statement)


async def service_for_create_folder(session: AsyncSession) -> db.Service:
    statement = (
        sqlalchemy.select(db.Service)
        .options(selectinload(db.Service.service_space))
        .where(db.Service.status == enums.ServiceStatus.NEED_CREATE_RELEASE_FOLDER)
        .with_for_update()
    )
    return await session.scalar(statement=statement)


async def service_with_space(
    session: AsyncSession,
    service_id: uuid.UUID,
) -> db.Service | None:
    statement = (
        sqlalchemy.select(db.Service)
        .options(selectinload(db.Service.service_space))
        .where(db.Service.id == service_id)
        .with_for_update()
    )
    return await session.scalar(statement=statement)

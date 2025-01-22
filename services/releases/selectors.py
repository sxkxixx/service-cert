import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from common import db, enums


async def select_releases(
    name: str | None,
    offset: int,
    limit: int,
) -> list[db.Release]:
    stmt = sqlalchemy.select(db.Release).offset(offset=offset).limit(limit=limit)

    if name is not None:
        stmt = stmt.filter(db.Release.name.like(name))

    async with db.AsyncSession() as session:
        result = await session.execute(statement=stmt)
    return result.scalars().all()


async def get_release_by_id(release_id: uuid.UUID) -> db.Release | None:
    async with db.AsyncSession() as session:
        statement = (
            sqlalchemy.select(db.Release)
            .where(db.Release.id == release_id)
            .options(selectinload(db.Release.release_requirements))
        )
        return await session.scalar(statement=statement)


async def get_full_release_info(release_id: uuid.UUID) -> db.Release | None:
    async with db.AsyncSession() as session:
        statement = (
            sqlalchemy.select(db.Release)
            .where(db.Release.id == release_id)
            .options(
                selectinload(db.Release.release_requirements),
                selectinload(db.Release.release_page),
            )
        )
        return await session.scalar(statement=statement)


def get_release_with_requirements(
    release_id: uuid.UUID, lock: bool = False
) -> sqlalchemy.Select[db.Release]:
    query = (
        sqlalchemy.select(db.Release)
        .where(db.Release.id == release_id)
        .options(selectinload(db.Release.release_requirements))
    )
    if lock:
        return query.with_for_update()
    return query


def get_release_stmt(release_id: uuid.UUID, lock: bool = False) -> sqlalchemy.Select[db.Release]:
    query = sqlalchemy.select(db.Release).where(db.Release.id == release_id)
    if lock:
        return query.with_for_update()
    return query


def get_release_with_service_stmt(
    release_id: uuid.UUID, lock: bool = False
) -> sqlalchemy.Select[db.Release]:
    query = (
        sqlalchemy.select(db.Release)
        .options(selectinload(db.Release.service))
        .where(db.Release.id == release_id)
    )
    if lock:
        return query.with_for_update()
    return query


async def get_releases_by_service_id(service_id: uuid.UUID) -> list[db.Release]:
    statement = (
        sqlalchemy.select(db.Release)
        .where(db.Release.service_id == service_id)
        .order_by(db.Release.created_at)
    )
    async with db.AsyncSession() as session:
        return await session.scalars(statement=statement)


def release_for_create_page_stmt(session: AsyncSession, lock: bool = False) -> sqlalchemy.Select:
    stmt = (
        sqlalchemy.select(db.Release).where(db.Release.status == enums.ReleaseStatus.NEW).limit(1)
    )
    if lock:
        stmt = stmt.with_for_update()
    return stmt

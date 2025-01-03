import uuid

import sqlalchemy
from sqlalchemy.orm import selectinload

from common import db


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

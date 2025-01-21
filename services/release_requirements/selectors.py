import uuid

import sqlalchemy

from common import db


async def select_all(limit: int, offset: int) -> list[db.ReleaseRequirement]:
    statement = (
        sqlalchemy.select(db.ReleaseRequirement).distinct().offset(offset=offset).limit(limit=limit)
    )

    async with db.AsyncSession() as session:
        requirement_names = await session.scalars(statement=statement)
    return requirement_names


def get_by_id_stmt(requirement_id: uuid.UUID, lock: bool = False) -> sqlalchemy.Select:
    query = sqlalchemy.select(db.ReleaseRequirement).where(
        db.ReleaseRequirement.id == requirement_id
    )
    if lock:
        return query.with_for_update()
    return query


async def get_release_requirement_by_release_id(
    release_id: uuid.UUID,
) -> list[db.ReleaseRequirement]:
    statement = sqlalchemy.select(db.ReleaseRequirement).where(
        db.ReleaseRequirement.release_id == release_id
    )
    async with db.AsyncSession() as session:
        return await session.scalars(statement=statement)

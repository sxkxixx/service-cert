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

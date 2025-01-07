import uuid

import sqlalchemy

from common import db


async def select_all(limit: int, offset: int) -> list[str]:
    statement = (
        sqlalchemy.select(db.ServiceRequirement.name)
        .distinct()
        .offset(offset=offset)
        .limit(limit=limit)
    )

    async with db.AsyncSession() as session:
        requirement_names = await session.scalars(statement=statement)
    return requirement_names


def get_by_id_stmt(requirement_id: uuid.UUID, lock: bool = False) -> sqlalchemy.Select:
    query = sqlalchemy.select(db.ServiceRequirement).where(
        db.ServiceRequirement.id == requirement_id
    )
    if lock:
        return query.with_for_update()
    return query

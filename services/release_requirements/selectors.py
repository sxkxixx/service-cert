import sqlalchemy

from common import db


async def select_all(limit: int, offset: int) -> list[str]:
    statement = (
        sqlalchemy.select(db.ReleaseRequirement.name)
        .distinct()
        .offset(offset=offset)
        .limit(limit=limit)
    )

    async with db.AsyncSession() as session:
        requirement_names = await session.scalars(statement=statement)
    return requirement_names

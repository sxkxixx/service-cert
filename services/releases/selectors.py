import sqlalchemy

from common import db


async def select_releases(
    name: str | None,
    offset: int,
    limit: int,
) -> list[db.Release]:
    stmt = (
        sqlalchemy.select(db.Release)
        .offset(offset=offset)
        .limit(limit=limit)
    )

    if name is not None:
        stmt = stmt.filter(db.Release.name.like(name))

    async with db.AsyncSession() as session:
        result = await session.execute(statement=stmt)
    return result.scalars().all()

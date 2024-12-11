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

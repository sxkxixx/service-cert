import sqlalchemy

from common import db


async def create_service(name: str, description: str | None) -> db.Service:
    statement = (
        sqlalchemy.insert(db.Service)
        .values(
            name=name,
            description=description,
        )
        .returning(db.Service)
    )

    async with db.transaction() as session:
        service = await session.scalar(statement=statement)
    return service

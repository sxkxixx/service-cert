import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common.db import Service, transaction


async def create_service(**kwargs) -> Service:
    async with transaction() as tsx:
        tsx: AsyncSession
        stmt = sqlalchemy.insert(Service).values(**kwargs).returning(Service)
        service = await tsx.scalar(statement=stmt)
    return service

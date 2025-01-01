import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from common import db
from services import exceptions


async def create_service(
    name: str,
    description: str | None,
    requirements: list,
) -> db.Service:
    async with db.transaction() as session:
        session: AsyncSession
        statement = (
            sqlalchemy.insert(db.Service)
            .values(name=name, description=description)
            .returning(db.Service)
        )
        service = await session.scalar(statement=statement)
        for requirement in requirements:
            await session.scalar(
                sqlalchemy.insert(db.ServiceRequirement)
                .values(
                    service_id=service.id,
                    name=requirement.name,
                    value=requirement.value,
                )
                .returning(db.ServiceRequirement)
            )
        return await session.scalar(
            sqlalchemy.select(db.Service)
            .filter(db.Service.id == service.id)
            .options(selectinload(db.Service.service_requirements))
        )


def service_statement(service_id: uuid.UUID, lock: bool = False) -> sqlalchemy.Select:
    query = sqlalchemy.select(db.Service).filter(db.Service.id == service_id)
    if lock:
        return query.with_for_update()
    return query


def _service_with_requirements_query(
    service_id: uuid.UUID, lock: bool = False
) -> sqlalchemy.Select:
    query: sqlalchemy.Select = (
        sqlalchemy.select(db.Service)
        .options(selectinload(db.Service.service_requirements))
        .filter(db.Service.id == service_id)
    )
    if lock:
        query = query.with_for_update()
    return query


async def create_service_from_another(
    name: str,
    description: str | None,
    source_service_id: uuid.UUID,
) -> db.Service:
    async with db.transaction() as session:
        source_service = await session.scalar(
            statement=_service_with_requirements_query(service_id=source_service_id, lock=True)
        )
        if source_service is None:
            raise exceptions.ServiceNotFound()
        new_service = await session.scalar(
            sqlalchemy.insert(db.Service)
            .values(
                name=name,
                description=description,
            )
            .returning(db.Service)
        )
        for req in source_service.service_requirements:
            await session.scalar(
                sqlalchemy.insert(db.ServiceRequirement)
                .values(name=req.name, value=None, service_id=new_service.id)
                .returning(db.ServiceRequirement)
            )

        return await session.scalar(
            statement=_service_with_requirements_query(service_id=new_service.id)
        )

import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from common import db, enums
from services import exceptions
from services.service import selectors as service_selectors


async def create_service(
    name: str,
    description: str | None,
    requirements: list,
) -> db.Service:
    async with db.transaction() as session:
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
                .values(name=req.name, value=None, service_id=new_service.id, type=req.type)
                .returning(db.ServiceRequirement)
            )

        return await session.scalar(
            statement=_service_with_requirements_query(service_id=new_service.id)
        )


async def create_release_requirement(
    service_id: uuid.UUID,
    responsible_id: uuid.UUID,
    requirement,
) -> db.ServiceRequirement:
    async with db.transaction() as session:
        service = await session.scalar(
            statement=service_selectors.get_service_stmt(
                service_id=service_id,
                lock=True,
            ),
        )
        if service is None:
            raise exceptions.ServiceNotFound()
        insert_stmt = (
            sqlalchemy.insert(db.ServiceRequirement)
            .values(
                responsible_id=responsible_id,
                service_id=service.id,
                name=requirement.name,
                value=requirement.value,
            )
            .returning(db.ServiceRequirement)
        )
        return await session.scalar(statement=insert_stmt)


async def mark_service_as_generating_space_process(
    session: AsyncSession,
    service: db.Service,
) -> db.Service:
    return await set_service_status(
        session=session, service=service, status=enums.ServiceStatus.GENERATING_CONFLUENCE_SPACE
    )


async def mark_service_need_update_homepage(
    session: AsyncSession, service: db.Service
) -> db.Service:
    return await set_service_status(
        session=session, service=service, status=enums.ServiceStatus.NEED_UPDATE_HOMEPAGE
    )


async def set_service_status(
    session: AsyncSession,
    service: db.Service,
    status: enums.ServiceStatus,
) -> db.Service:
    statement = (
        sqlalchemy.update(db.Service)
        .where(db.Service.id == service.id)
        .values(status=status)
        .returning(db.Service)
    )
    return await session.scalar(statement=statement)

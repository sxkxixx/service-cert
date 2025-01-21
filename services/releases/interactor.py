import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common import db, enums
from common.schemas.requirement import RequirementCreate
from services import exceptions
from services.service.selectors import get_service_stmt

from ..exceptions import ReleaseNotFound, ServiceNotFound
from .selectors import get_release_with_requirements


async def create_release(
    service_id: uuid.UUID,
    name: str,
    semantic_version: str | None,
    requirements: list[RequirementCreate],
) -> db.Release:
    async with db.transaction() as session:
        service = await session.scalar(get_service_stmt(service_id=service_id, lock=True))
        if service is None:
            raise exceptions.ServiceNotFound()
        release = await session.scalar(
            sqlalchemy.insert(db.Release)
            .values(
                service_id=service_id,
                name=name,
                semantic_version=semantic_version,
            )
            .returning(db.Release)
        )
        for req in requirements:
            await session.scalar(
                sqlalchemy.insert(db.ReleaseRequirement)
                .values(
                    release_id=release.id,
                    name=req.name,
                    value=req.value,
                )
                .returning(db.ReleaseRequirement)
            )
        return await session.scalar(statement=get_release_with_requirements(release_id=release.id))


async def create_release_from_another(
    name: str,
    semantic_version: str | None,
    service_id: uuid.UUID,
    source_release_id: uuid.UUID,
) -> db.Release:
    async with db.transaction() as session:
        session: AsyncSession
        service = await session.scalar(statement=get_service_stmt(service_id=service_id, lock=True))
        if service is None:
            raise ServiceNotFound()
        source_release: db.Release = await session.scalar(
            statement=get_release_with_requirements(
                release_id=source_release_id,
                lock=True,
            )
        )
        if source_release is None:
            raise ReleaseNotFound()
        new_release = await session.scalar(
            statement=(
                sqlalchemy.insert(db.Release)
                .values(
                    service_id=service.id,
                    name=name,
                    semantic_version=semantic_version,
                )
                .returning(db.Release)
            ),
        )
        for req in source_release.release_requirements:
            await session.scalar(
                statement=(
                    sqlalchemy.insert(db.ReleaseRequirement)
                    .values(name=req.name, value=None, release_id=new_release.id)
                    .returning(db.ReleaseRequirement)
                ),
            )
        return await session.scalar(
            statement=get_release_with_requirements(release_id=new_release.id)
        )


async def set_release_status(
    session: AsyncSession,
    release: db.Release,
    status: enums.ReleaseStatus,
) -> db.Release:
    statement = (
        sqlalchemy.update(db.Release)
        .where(db.Release.id == release.id)
        .values(status=status)
        .returning(db.Release)
    )
    return await session.scalar(statement=statement)

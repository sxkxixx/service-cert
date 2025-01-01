import uuid

import sqlalchemy
from sqlalchemy.orm import selectinload

from common import db
from common.schemas.requirement import RequirementCreate
from services import exceptions
from services.service.interactor import service_statement


def release_with_requirements_stmt(release_id: uuid.UUID, lock: bool = False) -> sqlalchemy.Select:
    query = (
        sqlalchemy.select(db.Release)
        .where(db.Release.id == release_id)
        .options(selectinload(db.Release.release_requirements))
    )
    if lock:
        return query.with_for_update()
    return query


async def create_release(
    service_id: uuid.UUID,
    name: str,
    semantic_version: str | None,
    requirements: list[RequirementCreate],
) -> db.Release:
    async with db.transaction() as session:
        service = await session.scalar(service_statement(service_id=service_id, lock=True))
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
        return await session.scalar(release_with_requirements_stmt(release_id=release.id))

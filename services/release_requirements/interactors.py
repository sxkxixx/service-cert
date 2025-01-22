import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common import db
from services.exceptions import ReleaseNotFound, RequirementNotFound
from services.releases import selectors as release_selectors

from . import selectors


async def edit_release_requirement(
    requirement_id: uuid.UUID,
    name: str,
    responsible_id: uuid.UUID,
    value: str | None,
    _type: str | None,
) -> db.ReleaseRequirement:
    async with db.transaction() as session:
        requirement = await session.scalar(
            selectors.get_by_id_stmt(requirement_id=requirement_id, lock=True)
        )
        if requirement is None:
            raise RequirementNotFound()
        update_stmt = (
            sqlalchemy.update(db.ReleaseRequirement)
            .where(db.ReleaseRequirement.id == requirement_id)
            .values(name=name, value=value, type=_type, responsible_id=responsible_id)
            .returning(db.ReleaseRequirement)
        )
        return await session.scalar(statement=update_stmt)


async def delete_release_requirement(requirement_id: uuid.UUID) -> None:
    async with db.transaction() as session:
        requirement = await session.scalar(
            selectors.get_by_id_stmt(requirement_id=requirement_id, lock=True)
        )
        if requirement is None:
            raise RequirementNotFound()
        delete_stmt = (
            sqlalchemy.delete(db.ReleaseRequirement)
            .where(db.ReleaseRequirement.id == requirement_id)
            .returning(db.ReleaseRequirement.id)
        )
        await session.scalar(statement=delete_stmt)


async def create_release_requirement(
    release_id: uuid.UUID,
    responsible_id: uuid.UUID,
    requirement,
) -> db.ReleaseRequirement:
    async with db.transaction() as session:
        release = await session.scalar(
            statement=release_selectors.get_release_stmt(
                release_id=release_id,
                lock=True,
            ),
        )
        if release is None:
            raise ReleaseNotFound()
        insert_stmt = (
            sqlalchemy.insert(db.ReleaseRequirement)
            .values(
                responsible_id=responsible_id,
                release_id=release.id,
                name=requirement.name,
                value=requirement.value,
                type=requirement.type,
            )
            .returning(db.ReleaseRequirement)
        )
        return await session.scalar(statement=insert_stmt)

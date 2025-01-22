import uuid

import sqlalchemy

from common import db
from services.exceptions import RequirementNotFound

from . import selectors


async def edit_service_requirement(
    requirement_id: uuid.UUID,
    name: str,
    value: str | None,
    _type: str | None,
) -> db.ServiceRequirement:
    async with db.transaction() as session:
        requirement = await session.scalar(
            selectors.get_by_id_stmt(requirement_id=requirement_id, lock=True)
        )
        if requirement is None:
            raise RequirementNotFound()
        update_stmt = (
            sqlalchemy.update(db.ServiceRequirement)
            .where(db.ServiceRequirement.id == requirement_id)
            .values(name=name, value=value, type=_type)
            .returning(db.ServiceRequirement)
        )
        return await session.scalar(statement=update_stmt)


async def delete_service_requirement(requirement_id: uuid.UUID) -> None:
    async with db.transaction() as session:
        requirement = await session.scalar(
            selectors.get_by_id_stmt(requirement_id=requirement_id, lock=True)
        )
        if requirement is None:
            raise RequirementNotFound()
        delete_stmt = (
            sqlalchemy.delete(db.ServiceRequirement)
            .where(db.ServiceRequirement.id == requirement_id)
            .returning(db.ServiceRequirement.id)
        )
        await session.scalar(statement=delete_stmt)

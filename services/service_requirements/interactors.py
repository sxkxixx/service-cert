import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common import db

from ..exceptions import RequirementNotFound
from . import selectors


async def edit_service_requirement(
    requirement_id: uuid.UUID,
    name: str,
    value: str | None,
) -> db.ServiceRequirement:
    async with db.transaction() as session:
        requirement = await session.scalar(selectors.get_by_id_stmt(requirement_id=requirement_id, lock=True))
        if requirement is None:
            raise RequirementNotFound()
        update_stmt = (
            sqlalchemy.update(db.ServiceRequirement)
            .where(db.ServiceRequirement.id == requirement_id)
            .values(name=name, value=value)
            .returning(db.ServiceRequirement)
        )
        return await session.scalar(statement=update_stmt)

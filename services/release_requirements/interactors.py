import uuid

import sqlalchemy

from common import db

from ..exceptions import RequirementNotFound
from . import selectors


async def edit_release_requirement(
    requirement_id: uuid.UUID,
    name: str,
    value: str | None,
) -> db.ReleaseRequirement:
    async with db.transaction() as session:
        requirement = await session.scalar(selectors.get_by_id_stmt(requirement_id=requirement_id, lock=True))
        if requirement is None:
            raise RequirementNotFound()
        update_stmt = (
            sqlalchemy.update(db.ReleaseRequirement)
            .where(db.ReleaseRequirement.id == requirement_id)
            .values(name=name, value=value)
            .returning(db.ReleaseRequirement)
        )
        return await session.scalar(statement=update_stmt)

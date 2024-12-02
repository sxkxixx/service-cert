import logging

import sqlalchemy

from common import db

logger = logging.getLogger(__name__)


async def select_templates(
    limit: int,
    offset: int,
) -> list[db.Template]:
    async with db.session_factory() as session:
        query = (
            sqlalchemy.select(db.Template)
            .join(db.Template.requirements)
            .offset(offset=offset)
            .limit(limit=limit)
        )
        logger.debug(query)
        result = await session.execute(statement=query)
    return result

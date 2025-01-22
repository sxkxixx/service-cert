import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common import db


async def create_release_page(
    session: AsyncSession,
    release: db.Release,
    service_space: db.ServiceSpace,
    page_id: str,
    webui_link: str,
) -> db.ReleasePage:
    statement = (
        sqlalchemy.insert(db.ReleasePage)
        .values(
            service_space_id=service_space.id,
            release_id=release.id,
            page_id=page_id,
            webui_link=webui_link,
        )
        .returning(db.ReleasePage)
    )
    return await session.scalar(statement=statement)

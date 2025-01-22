import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common import db


async def create_service_space(
    session: AsyncSession,
    service: db.Service,
    ext_id: int,
    homepage_id: int,
    webui_link: str,
    key_alias: str,
) -> db.ServiceSpace:
    statement = (
        sqlalchemy.insert(db.ServiceSpace)
        .values(
            service_id=service.id,
            webui_link=webui_link,
            ext_id=ext_id,
            key=key_alias,
            alias=key_alias,
            homepage_id=homepage_id,
        )
        .returning(db.ServiceSpace)
    )
    return await session.scalar(statement=statement)


async def update_service_space(
    session: AsyncSession,
    service_space: db.ServiceSpace,
    release_folder_id: str,
) -> db.ServiceSpace:
    statement = (
        sqlalchemy.update(db.ServiceSpace)
        .values(release_folder_id=release_folder_id)
        .where(db.ServiceSpace.id == service_space.id)
        .returning(db.ServiceSpace)
    )
    return await session.scalar(statement=statement)

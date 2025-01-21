import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common import db
from services import exceptions as service_exc
from services.service import selectors as service_selectors
from services.user import selectors as user_selectors


async def remove_teammates_by_service(
    session: AsyncSession,
    service_id: db.Service,
) -> None:
    statement = (
        sqlalchemy.delete(db.Teammate)
        .where(db.Teammate.service_id.__eq__(service_id))
        .returning(db.Teammate)
    )
    await session.scalar(statement=statement)


async def set_teammates(
    session: AsyncSession,
    service: db.Service,
    users: list[db.User],
) -> list[db.Teammate]:
    result = []
    for user in users:
        statement = (
            sqlalchemy.insert(db.Teammate)
            .values(
                user_id=user.id,
                service_id=service.id,
            )
            .returning(db.Teammate)
        )
        teammate = await session.scalar(statement=statement)
        result.append(teammate)
    return result


async def edit_service_teammates(
    service_id: uuid.UUID,
    teammates_ids: list[uuid.UUID],
) -> list[db.Teammate]:
    async with db.transaction() as session:
        service = await session.scalar(
            statement=service_selectors.get_service_stmt(
                service_id=service_id,
                lock=True,
            ),
        )
        if service is None:
            raise service_exc.ServiceNotFound()
        users = await session.scalars(
            statement=user_selectors.get_users_by_ids_stmt(
                users_ids=teammates_ids,
                lock=True,
            ),
        )
        await remove_teammates_by_service(session=session, service_id=service_id)
        return await set_teammates(session=session, service=service, users=users)

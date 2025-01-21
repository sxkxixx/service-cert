import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common import db


async def get_user_by_email_or_nickname(factor: str) -> db.User | None:
    statement = sqlalchemy.select(db.User).filter(
        sqlalchemy.or_(db.User.email == factor, db.User.nickname == factor)
    )

    async with db.AsyncSession() as session:
        user = await session.scalar(statement=statement)
    return user


async def get_user_by_id(id: str) -> db.User | None:
    statement = sqlalchemy.select(db.User).filter(db.User.id == id)

    async with db.AsyncSession() as session:
        user = await session.scalar(statement=statement)
    return user


async def assert_user_exists(user_id: uuid.UUID) -> None:
    statement = sqlalchemy.select(db.User).filter(db.User.id == user_id)
    async with db.AsyncSession() as session:
        assert bool(await session.scalar(statement=statement))


async def get_all() -> list[db.User]:
    statement = sqlalchemy.select(db.User)
    async with db.AsyncSession() as session:
        return await session.scalars(statement=statement)


def get_users_by_ids_stmt(
    users_ids: list[uuid.UUID],
    lock: bool = False,
) -> sqlalchemy.Select:
    statement = sqlalchemy.select(db.User).where(db.User.id.in_(users_ids))
    if lock:
        statement = statement.with_for_update()
    return statement

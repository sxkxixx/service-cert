import uuid

import sqlalchemy

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

import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from common import db, hasher


async def create_user(
    *,
    name: str,
    nickname: str,
    email: str,
    password: str,
) -> db.User:
    statement = (
        sqlalchemy.insert(db.User)
        .values(
            name=name,
            nickname=nickname,
            email=email,
            password=hasher.get_password_hash(password=password),
        )
        .returning(db.User)
    )

    async with db.AsyncSession() as session:
        user = await session.scalar(statement=statement)

    return user


def get_user_dict(user: db.User) -> dict:
    return {
        'id': str(user.id),
        'name': user.name,
        'nickname': user.nickname,
        'email': user.email,
    }


async def delete_user(user_id: uuid.UUID) -> None:
    async with db.transaction() as session:
        session: AsyncSession
        statement = sqlalchemy.select(db.User).where(db.User.id == user_id).with_for_update()
        user = await session.scalar(statement=statement)
        if user is None:
            return
        delete_statement = sqlalchemy.delete(db.User).where(db.User.id == user_id)
        await session.execute(delete_statement)

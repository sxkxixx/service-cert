import sqlalchemy

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

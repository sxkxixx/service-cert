import sqlalchemy

from common import db, hasher


async def create_user(
    *,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
) -> db.User:
    statement = sqlalchemy.insert(db.User).values(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hasher.get_password_hash(password=password),
    ).returning(db.User)

    async with db.AsyncSession() as session:
        user = await session.scalar(statement=statement)

    return user


def get_user_dict(user: db.User) -> dict:
    return {
        'id': str(user.id),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

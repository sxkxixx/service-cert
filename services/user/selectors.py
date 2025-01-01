import sqlalchemy

from common import db


async def get_user_by_email(email: str) -> db.User | None:
    statement = sqlalchemy.select(db.User).filter(db.User.email == email)

    async with db.AsyncSession() as session:
        user = await session.scalar(statement=statement)
    return user

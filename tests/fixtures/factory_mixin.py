import typing

from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from common import db


class AsyncPersistenceAlchemyMixin:
    """Миксин для сохранения объектов в БД."""

    async def save(self, data: db.BaseModel) -> db.BaseModel:
        async with db.AsyncSession() as session:
            session.add(data)
            await session.commit()
            await session.refresh(data)
        return data

    async def save_many(self, data: list[db.BaseModel]) -> list[db.BaseModel]:
        async with db.AsyncSession() as session:
            session.add_all(data)
            await session.commit()
        return data


T = typing.TypeVar('T', bound=db.BaseModel)


class CustomSQLAlchemyFactory(typing.Generic[T], SQLAlchemyFactory[T]):
    __is_base_factory__ = True

    @classmethod
    def author_id(cls) -> None:
        pass

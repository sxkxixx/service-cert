import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory


class AsyncServicePersistence(
    AsyncPersistenceAlchemyMixin,
    AsyncPersistenceProtocol[db.Service],
):
    pass


class ServiceFactory(CustomSQLAlchemyFactory[db.Service]):
    __model__ = db.Service
    __async_persistence__ = AsyncServicePersistence


@pytest.fixture()
async def service() -> db.Service:
    return await ServiceFactory.create_async()

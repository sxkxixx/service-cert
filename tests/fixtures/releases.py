import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory


class AsyncReleasePersistence(
    AsyncPersistenceAlchemyMixin,
    AsyncPersistenceProtocol[db.Release]
):
    pass


class ReleaseFactory(CustomSQLAlchemyFactory[db.Release]):
    __model__ = db.Release
    __async_persistence__ = AsyncReleasePersistence


@pytest.fixture
async def release(service: db.Service, template: db.Template) -> db.Release:
    return await ReleaseFactory.create_async(service=service, template=template, semantic_version=None)

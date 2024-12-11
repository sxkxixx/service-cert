import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory


class AsyncTemplatePersistence(
    AsyncPersistenceAlchemyMixin,
    AsyncPersistenceProtocol[db.Template],
):
    pass


class TemplateFactory(CustomSQLAlchemyFactory[db.Template]):
    __model__ = db.Template
    __async_persistence__ = AsyncTemplatePersistence


@pytest.fixture()
async def template() -> db.Template:
    return await TemplateFactory.create_async()

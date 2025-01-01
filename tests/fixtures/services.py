import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory
from .service_requirements import ServiceRequirementFactory


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
    return await ServiceFactory.create_async(confluence_page_link=None)


@pytest.fixture()
async def service_with_requirement(service: db.Service) -> db.Service:
    await ServiceRequirementFactory.create_async(service_id=service.id, name='Требование сервиса')
    return service

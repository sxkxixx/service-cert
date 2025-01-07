import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory


class AsyncServiceRequirementPersistence(
    AsyncPersistenceAlchemyMixin,
    AsyncPersistenceProtocol[db.ServiceRequirement],
):
    pass


class ServiceRequirementFactory(CustomSQLAlchemyFactory[db.ServiceRequirement]):
    __model__ = db.ServiceRequirement
    __async_persistence__ = AsyncServiceRequirementPersistence


@pytest.fixture()
async def service_requirement(service) -> db.ServiceRequirement:
    return await ServiceRequirementFactory.create_async(service_id=service.id)

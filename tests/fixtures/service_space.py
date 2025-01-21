import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory


class AsyncServiceSpacePersistence(
    AsyncPersistenceAlchemyMixin,
    AsyncPersistenceProtocol[db.ServiceSpace],
):
    pass


class ServiceSpaceFactory(CustomSQLAlchemyFactory[db.ServiceSpace]):
    __model__ = db.ServiceSpace
    __async_persistence__ = AsyncServiceSpacePersistence


@pytest.fixture()
async def service_space(service_need_create_release_folder: db.Service) -> db.ServiceSpace:
    return await ServiceSpaceFactory.create_async(
        service_id=service_need_create_release_folder.id,
    )

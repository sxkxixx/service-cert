import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory
from .release_requirement import ReleaseRequirementFactory


class AsyncReleasePersistence(AsyncPersistenceAlchemyMixin, AsyncPersistenceProtocol[db.Release]):
    pass


class ReleaseFactory(CustomSQLAlchemyFactory[db.Release]):
    __model__ = db.Release
    __async_persistence__ = AsyncReleasePersistence


@pytest.fixture
async def release(service: db.Service) -> db.Release:
    return await ReleaseFactory.create_async(service=service, semantic_version=None)


@pytest.fixture()
async def release_with_requirements(release: db.Release) -> db.Release:
    await ReleaseRequirementFactory.create_async(
        release_id=release.id,
        name='Требование релиза',
        value='Значение требования релиза',
    )
    return release

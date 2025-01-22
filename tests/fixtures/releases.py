import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db, enums

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory
from .release_requirement import ReleaseRequirementFactory
from .service_space import ServiceSpaceFactory


class AsyncReleasePersistence(AsyncPersistenceAlchemyMixin, AsyncPersistenceProtocol[db.Release]):
    pass


class ReleaseFactory(CustomSQLAlchemyFactory[db.Release]):
    __model__ = db.Release
    __async_persistence__ = AsyncReleasePersistence


@pytest.fixture
async def release(service: db.Service) -> db.Release:
    return await ReleaseFactory.create_async(
        service=service,
        semantic_version=None,
        status=enums.ReleaseStatus.NEW,
        description=None,
    )


@pytest.fixture()
async def release_with_requirements(release: db.Release) -> db.Release:
    await ReleaseRequirementFactory.create_async(
        release_id=release.id,
        name='Требование релиза',
        value='Значение требования релиза',
        responsible_id=None,
        type=None,
    )
    return release


@pytest.fixture()
async def release_for_creating_page(
    release_with_requirements: db.Release,
    service: db.Service,
) -> db.Release:
    await ServiceSpaceFactory.create_async(service_id=release_with_requirements.service_id)
    return release_with_requirements

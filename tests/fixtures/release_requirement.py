import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory


class AsyncReleaseRequirementPersistence(
    AsyncPersistenceAlchemyMixin,
    AsyncPersistenceProtocol[db.ReleaseRequirement],
):
    pass


class ReleaseRequirementFactory(CustomSQLAlchemyFactory[db.ReleaseRequirement]):
    __model__ = db.ReleaseRequirement
    __async_persistence__ = AsyncReleaseRequirementPersistence


@pytest.fixture()
async def release_requirement(release: db.Release) -> db.ReleaseRequirement:
    return await ReleaseRequirementFactory.create_async(
        release_id=release.id, responsible_id=None, type=None
    )

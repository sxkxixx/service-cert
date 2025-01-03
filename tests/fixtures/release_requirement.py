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

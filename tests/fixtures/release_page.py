import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory


class AsyncReleasePagePersistence(
    AsyncPersistenceAlchemyMixin,
    AsyncPersistenceProtocol[db.ReleasePage],
):
    pass


class ReleasePageFactory(CustomSQLAlchemyFactory[db.ReleasePage]):
    __model__ = db.ReleasePage
    __async_persistence__ = AsyncReleasePagePersistence


@pytest.fixture()
async def release_page(
    release,
    service_space,
) -> db.ReleasePage:
    return await ReleasePageFactory.create_async(
        service_space_id=service_space.id,
        release_id=release.id,
        page_id='213123',
        webui_link='',
    )

import uuid
from unittest import mock

import pytest
import sqlalchemy

from common import db, enums
from jobs import background_tasks


@pytest.fixture()
def mock_create_page() -> mock.Mock:
    with mock.patch(
        'common.clients.confluence.ConfluenceClient.create_page',
        return_value={
            'parentType': 'page',
            'parentId': '22872325',
            'ownerId': '619e5952c510bc006b96a866',
            'lastOwnerId': None,
            'authorId': '619e5952c510bc006b96a866',
            'position': 40,
            'version': {
                'number': 1,
                'message': '',
                'minorEdit': False,
                'authorId': '619e5952c510bc006b96a866',
                'createdAt': '2025-01-21T17:08:52.778Z',
            },
            'body': {
                'storage': {
                    'representation': 'storage',
                    'value': '',
                }
            },
            'status': 'current',
            'title': 'TryingCreatePageFromApiV2',
            'spaceId': '22872069',
            'id': '27099137',
            '_links': {
                'editui': '/pages/resumedraft.action?draftId=27099137',
                'webui': '/spaces/1629741214551149e6fc2d00cdbd6dfb/pages/27099137/TryingCreatePageFromApiV2',
                'edituiv2': '/spaces/1629741214551149e6fc2d00cdbd6dfb/pages/edit-v2/27099137',
                'tinyui': '/x/AYCdAQ',
                'base': 'https://asemyonov.atlassian.net/wiki',
            },
        },
    ) as _mock_create_page:
        yield _mock_create_page


async def test_no_new_releases() -> None:
    with mock.patch('services.releases.interactor.set_release_status') as _mock:
        await background_tasks.generate_release_page.generate_page_for_release()
    _mock.assert_not_awaited()


async def get_release_page(release_id: uuid.UUID) -> db.ReleasePage | None:
    async with db.AsyncSession() as session:
        return await session.scalar(
            sqlalchemy.select(db.ReleasePage).where(db.ReleasePage.release_id == release_id)
        )


async def get_release(release_id: uuid.UUID) -> db.Release | None:
    async with db.AsyncSession() as session:
        return await session.scalar(
            statement=sqlalchemy.select(db.Release).where(db.Release.id == release_id)
        )


async def test_ok(release_for_creating_page: db.Release, mock_create_page: mock.Mock) -> None:
    await background_tasks.generate_release_page.generate_page_for_release()
    release_page = await get_release_page(release_id=release_for_creating_page.id)
    assert release_page is not None
    assert (
        release_page.webui_link
        == 'https://asemyonov.atlassian.net/wiki/spaces/1629741214551149e6fc2d00cdbd6dfb/pages/27099137/TryingCreatePageFromApiV2'
    )
    release = await get_release(release_for_creating_page.id)
    assert release.status == enums.ReleaseStatus.READY

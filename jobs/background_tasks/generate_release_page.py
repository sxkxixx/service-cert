import logging

from common import confluence, db, enums
from infrastructure.config import app_config
from jobs.utils.decorators import periodic_task_run
from services.release_page import interactor as release_page_interactor
from services.releases import interactor as release_interactor
from services.releases import selectors as release_selectors
from services.service_space import selectors as service_space_selectors

logger = logging.getLogger(__name__)


@periodic_task_run(sleep=app_config.BACKGROUND_TASK_PERIOD)
async def generate_page_for_release(*_args, **_kwargs) -> None:
    async with db.transaction() as session:
        release = await session.scalar(
            release_selectors.release_for_create_page_stmt(session=session, lock=True)
        )
        if release is None:
            logger.info('Not found releases for creating page')
            return
        await release_interactor.set_release_status(
            session=session,
            release=release,
            status=enums.ReleaseStatus.GENERATING_RELEASE_PAGE,
        )
        service_space = await session.scalar(
            statement=service_space_selectors.get_service_space_by_service_id(
                service_id=release.service_id,
                lock=False,
            ),
        )

    page = await confluence.page.create_page(release=release, service_space=service_space)

    async with db.transaction() as session:
        release = await session.scalar(
            statement=release_selectors.get_release_stmt(release_id=release.id, lock=True)
        )
        assert release, 'Release %s was deleted' % release.id
        service_space = await session.scalar(
            statement=service_space_selectors.get_service_space_by_service_id(
                service_id=release.service_id,
                lock=True,
            ),
        )
        assert service_space, 'Service space for service %s not found' % release.service_id
        await release_interactor.set_release_status(
            session=session,
            release=release,
            status=enums.ReleaseStatus.READY,
        )
        await release_page_interactor.create_release_page(
            session=session,
            release=release,
            service_space=service_space,
            page_id=page.id,
            webui_link=page.webui_url,
        )

import logging

from common import confluence, db
from infrastructure.config import app_config
from jobs.utils.decorators import periodic_task_run
from services.service import interactor as service_interactor
from services.service import selectors as service_selectors
from services.service_space import interactor as service_space_interactor

logger = logging.getLogger(__name__)


@periodic_task_run(sleep=app_config.BACKGROUND_TASK_PERIOD)
async def init_generate_space(*_args, **_kwargs) -> None:
    async with db.transaction() as session:
        service = await service_selectors.get_service_for_generate_space(session=session, lock=True)
        if service is None:
            logger.info('No services in status "new"')
            return
        logger.info('Mark service id=%s as generating_confluence_space')
        await service_interactor.mark_service_as_generating_space_process(
            session=session, service=service
        )


@periodic_task_run(sleep=app_config.BACKGROUND_TASK_PERIOD)
async def generate_space(*_args, **_kwargs) -> None:
    async with db.AsyncSession() as session:
        service = await service_selectors.get_service_ready_to_generate_space(session=session)
        if service is None:
            logger.info('No services in status "generating_confluence_space"')
            return

    logger.info('Generating space for service id=%s', service.id)
    service_space = await confluence.space.create_service_space(service=service)
    logger.info('Space for service id=%s created', service_space.id)

    async with db.transaction() as session:
        service = await session.scalar(
            statement=service_selectors.get_service_stmt(service_id=service.id, lock=True)
        )
        await service_interactor.mark_need_create_release_folder(session=session, service=service)
        await service_space_interactor.create_service_space(
            session=session,
            service=service,
            webui_link=service_space.webui_url,
            ext_id=service_space.id,
            key_alias=service_space.key,
            homepage_id=service_space.homepage_id,
        )

import logging

from common import confluence, const, db, enums
from infrastructure.config import app_config
from jobs.utils.decorators import periodic_task_run
from services.service import interactor as service_interactor
from services.service import selectors as service_selectors
from services.service_space import interactor as service_space_interactor

logger = logging.getLogger(__name__)


@periodic_task_run(sleep=app_config.BACKGROUND_TASK_PERIOD)
async def create_release_folder(*_args, **_kwargs) -> None:
    async with db.transaction() as session:
        service = await service_selectors.service_for_create_folder(session=session)
        if service is None:
            logger.info('Not found services to create release folder')
            return
        service = await service_interactor.set_service_status(
            session=session,
            service=service,
            status=enums.ServiceStatus.CREATING_RELEASE_FOLDER,
        )
        logger.info('service id=%s moved to status creating_release_folder')

    service_space = service.service_space
    folder = await confluence.folder.create_folder(
        space_id=str(service_space.ext_id),
        title=const.DEFAULT_RELEASE_FOLDER_NAME,
    )

    async with db.transaction() as session:
        service = await service_selectors.service_with_space(session=session, service_id=service.id)
        await service_space_interactor.update_service_space(
            session=session,
            service_space=service.service_space,
            release_folder_id=folder.id,
        )
        await service_interactor.set_service_status(
            session=session,
            service=service,
            status=enums.ServiceStatus.NEED_UPDATE_HOMEPAGE,
        )

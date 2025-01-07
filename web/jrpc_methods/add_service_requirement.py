import uuid

import fastapi

from common import db
from common.schemas.requirement import Requirement, RequirementCreate
from services import exceptions as service_exc
from services.service import interactor as sr_interactor
from web import exceptions as web_exc
from web.dependencies.user import get_current_user

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
)
async def add_service_requirement(
    service_id: uuid.UUID,
    requirement: RequirementCreate,
    user: db.User = fastapi.Depends(get_current_user),
) -> Requirement:
    try:
        requirement = await sr_interactor.create_release_requirement(
            service_id=service_id,
            responsible_id=user.id,
            requirement=requirement,
        )
    except service_exc.ServiceNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return Requirement.model_validate(requirement, from_attributes=True)

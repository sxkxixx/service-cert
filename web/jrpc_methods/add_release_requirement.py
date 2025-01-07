import uuid

import fastapi

from common import db
from common.schemas.requirement import Requirement, RequirementCreate
from services import exceptions as service_exc
from services.release_requirements import interactors as rr_interactor
from web import exceptions as web_exc
from web.dependencies.user import get_current_user

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
)
async def add_release_requirement(
    release_id: uuid.UUID,
    requirement: RequirementCreate,
    user: db.User = fastapi.Depends(get_current_user),
) -> Requirement:
    try:
        requirement = await rr_interactor.create_release_requirement(
            release_id=release_id,
            responsible_id=user.id,
            requirement=requirement,
        )
    except service_exc.ReleaseNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return Requirement.model_validate(requirement, from_attributes=True)

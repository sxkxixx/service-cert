import uuid

import fastapi

from common.schemas.requirement import Requirement
from services import exceptions as service_exc
from services.release_requirements import interactors as rr_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
    errors=[web_exc.ObjectDoesNotExistsError],
)
async def edit_release_requirement(
    requirement_id: uuid.UUID,
    name: str,
    responsible_id: uuid.UUID,
    value: str | None = None,
    type_: str | None = fastapi.Query(default=None, alias='type'),
) -> Requirement:
    try:
        requirement = await rr_interactor.edit_release_requirement(
            requirement_id=requirement_id,
            name=name,
            value=value,
            _type=type_,
            responsible_id=responsible_id,
        )
    except service_exc.RequirementNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return Requirement.model_validate(requirement, from_attributes=True)

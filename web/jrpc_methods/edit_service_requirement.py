import uuid

import fastapi

from common.schemas.requirement import Requirement
from services import exceptions as service_exc
from services.service_requirements import interactors as sr_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
    errors=[web_exc.ObjectDoesNotExistsError],
)
async def edit_service_requirement(
    requirement_id: uuid.UUID,
    name: str,
    value: str | None = None,
    type_: str | None = fastapi.Query(default=None, alias='type'),
) -> Requirement:
    try:
        requirement = await sr_interactor.edit_service_requirement(
            requirement_id=requirement_id,
            name=name,
            value=value,
            _type=type_,
        )
    except service_exc.RequirementNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return Requirement.model_validate(requirement, from_attributes=True)

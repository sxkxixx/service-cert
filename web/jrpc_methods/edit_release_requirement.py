import uuid

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
    value: str | None = None,
) -> Requirement:
    try:
        requirement = await rr_interactor.edit_release_requirement(
            requirement_id=requirement_id,
            name=name,
            value=value,
        )
    except service_exc.RequirementNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return Requirement.model_validate(requirement, from_attributes=True)

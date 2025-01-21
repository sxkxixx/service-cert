import uuid

from common.schemas.team import Teammate
from services import exceptions as service_exc
from services.team import interactors as team_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['TEAM'],
    errors=[web_exc.ObjectDoesNotExistsError],
)
async def edit_service_team(
    service_id: uuid.UUID,
    teammates_ids: list[uuid.UUID],
) -> list[Teammate]:
    try:
        new_teammates = await team_interactor.edit_service_teammates(
            service_id=service_id,
            teammates_ids=teammates_ids,
        )
    except service_exc.ServiceNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return [Teammate.model_validate(teammate, from_attributes=True) for teammate in new_teammates]

import uuid

from services import exceptions as service_exc
from services.service_requirements import interactors as sr_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
)
async def delete_service_requirement(requirement_id: uuid.UUID) -> None:
    try:
        await sr_interactor.delete_service_requirement(requirement_id=requirement_id)
    except service_exc.RequirementNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return None

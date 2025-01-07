import uuid

from services import exceptions as service_exc
from services.release_requirements import interactors as rr_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
)
async def delete_release_requirement(requirement_id: uuid.UUID) -> None:
    try:
        await rr_interactor.delete_release_requirement(requirement_id=requirement_id)
    except service_exc.RequirementNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return None

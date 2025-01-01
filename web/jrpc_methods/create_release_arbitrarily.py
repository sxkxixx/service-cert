import uuid

from common.schemas.release import ReleaseResponse
from common.schemas.requirement import RequirementCreate
from services import exceptions as service_exc
from services.releases import interactor as release_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
    description='',
)
async def create_release_arbitrarily(
    service_id: uuid.UUID,
    name: str,
    semantic_version: str | None,
    requirements: list[RequirementCreate],
) -> ReleaseResponse:
    try:
        release = await release_interactor.create_release(
            service_id=service_id,
            name=name,
            semantic_version=semantic_version,
            requirements=requirements,
        )
    except service_exc.ServiceNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return ReleaseResponse.model_validate(release, from_attributes=True)

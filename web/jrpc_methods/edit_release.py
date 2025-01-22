import uuid

from common.schemas.release import ReleaseListResponse
from services import exceptions as service_exc
from services.releases import interactor as release_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
    errors=[web_exc.ObjectDoesNotExistsError],
)
async def edit_release(
    release_id: uuid.UUID,
    name: str,
    description: str,
    semantic_version: str | None = None,
) -> ReleaseListResponse:
    try:
        updated_release = await release_interactor.edit_release(
            release_id=release_id,
            name=name,
            description=description,
            semantic_version=semantic_version,
        )
    except service_exc.ReleaseNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return ReleaseListResponse.model_validate(updated_release, from_attributes=True)

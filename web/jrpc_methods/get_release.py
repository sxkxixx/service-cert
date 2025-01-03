import uuid

from common.schemas.release import ReleaseResponse
from services.releases import selectors as release_selectors
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
    errors=[web_exc.ObjectDoesNotExistsError],
)
async def get_release(release_id: uuid.UUID) -> ReleaseResponse:
    release = await release_selectors.get_release_by_id(release_id=release_id)
    if release is None:
        raise web_exc.ObjectDoesNotExistsError()
    return ReleaseResponse.model_validate(release, from_attributes=True)

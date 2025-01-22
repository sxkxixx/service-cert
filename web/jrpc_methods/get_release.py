import uuid

from common.schemas.release import FullReleaseResponse, ReleaseResponse
from services.releases import selectors as release_selectors
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
    errors=[web_exc.ObjectDoesNotExistsError],
)
async def get_release(release_id: uuid.UUID) -> FullReleaseResponse:
    release = await release_selectors.get_full_release_info(release_id=release_id)
    if release is None:
        raise web_exc.ObjectDoesNotExistsError()
    return FullReleaseResponse.model_validate(release, from_attributes=True)

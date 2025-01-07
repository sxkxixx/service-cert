import uuid

from common.schemas.release import ReleasesResponse
from services.releases import selectors as release_selectors

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
)
async def get_service_releases(service_id: uuid.UUID) -> ReleasesResponse:
    releases = await release_selectors.get_releases_by_service_id(service_id=service_id)
    return ReleasesResponse.model_validate(releases, from_attributes=True)

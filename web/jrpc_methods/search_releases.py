from common.schemas.batch import BatchQuery
from common.schemas.release import ReleasesResponse
from services.releases import selectors as releases_selectors

from ._rpc_server import rpc_server


@rpc_server.method()
async def search_releases(name: str | None, batch: BatchQuery) -> ReleasesResponse:
    releases = await releases_selectors.select_releases(name=name, offset=batch.offset, limit=batch.limit)
    return ReleasesResponse.model_validate(releases, from_attributes=True)

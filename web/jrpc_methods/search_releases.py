from common.schemas.batch import BatchQuery
from common.schemas.release import ReleasesResponse
from services.releases import selectors as releases_selectors

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
)
async def search_releases(batch: BatchQuery, name: str | None = None) -> ReleasesResponse:
    releases = await releases_selectors.select_releases(
        name=name,
        offset=batch.offset,
        limit=batch.limit,
    )
    return ReleasesResponse.model_validate(releases, from_attributes=True)

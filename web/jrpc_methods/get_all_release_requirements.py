from common.schemas.batch import BatchQuery
from services.release_requirements import selectors as rr_selectors

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
)
async def get_all_release_requirements(batch: BatchQuery) -> list[str]:
    requirements = await rr_selectors.select_all(limit=batch.limit, offset=batch.offset)
    return requirements

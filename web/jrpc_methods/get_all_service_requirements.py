from common.schemas.batch import BatchQuery
from services.service_requirements import selectors as sr_selectors

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
)
async def get_all_service_requirements(batch: BatchQuery) -> list[str]:
    return await sr_selectors.select_all(limit=batch.limit, offset=batch.offset)

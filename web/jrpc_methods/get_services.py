from common.schemas.batch import BatchQuery
from common.schemas.service import ServicesResponse
from services.service import selectors as service_selectors

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
    description='Select paginated services',
)
async def get_services(batch: BatchQuery) -> ServicesResponse:
    services = await service_selectors.get_services(offset=batch.offset, limit=batch.limit)
    return ServicesResponse.model_validate(services, from_attributes=True)

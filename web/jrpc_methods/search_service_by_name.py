from common.schemas.service import ServicesResponse
from services.service import selectors as service_selectors

from ._rpc_server import entrypoint


@entrypoint.method(tags=['SERVICE'])
async def search_service_by_name(name: str) -> ServicesResponse:
    services = await service_selectors.get_services_by_name(name=name)
    return ServicesResponse.model_validate(services, from_attributes=True)

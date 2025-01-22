import uuid

from common.schemas.service import FullServiceInfo, ServiceWithTeam
from services.service import selectors as service_selectors
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
    description='Get service by id',
    errors=[web_exc.ObjectDoesNotExistsError],
)
async def get_service(service_id: uuid.UUID) -> FullServiceInfo:
    service = await service_selectors.get_full_service_info(service_id=service_id)
    if service is None:
        raise web_exc.ObjectDoesNotExistsError()
    return FullServiceInfo.model_validate(service, from_attributes=True)

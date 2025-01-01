import uuid

from common.schemas.service import ServiceResponse
from services.service import selectors as service_selectors
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method()
async def get_service(service_id: uuid.UUID) -> ServiceResponse:
    service = await service_selectors.get_service(service_id=service_id)
    if service is None:
        raise web_exc.ObjectDoesNotExistsError()
    return ServiceResponse.model_validate(service, from_attributes=True)

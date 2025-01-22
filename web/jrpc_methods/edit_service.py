import uuid

from common.schemas.service import ServiceListResponse
from services import exceptions as service_exc
from services.service import interactor as service_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
)
async def edit_service(
    service_id: uuid.UUID,
    name: str,
    description: str,
) -> ServiceListResponse:
    try:
        updated_service = await service_interactor.update_service(
            service_id=service_id,
            name=name,
            description=description,
        )
    except service_exc.ServiceNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return ServiceListResponse.model_validate(updated_service, from_attributes=True)

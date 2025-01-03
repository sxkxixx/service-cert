from common.schemas.service import CreateServiceFromAnother, ServiceResponse
from services import exceptions as service_exc
from services.service import interactor as service_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['SERVICE'],
    description='Creating a new service, using requirements from another',
    errors=[web_exc.ObjectDoesNotExistsError],
)
async def create_service_by_another(service: CreateServiceFromAnother) -> ServiceResponse:
    try:
        service = await service_interactor.create_service_from_another(
            name=service.name,
            description=service.description,
            source_service_id=service.source_service_id,
        )
    except service_exc.ServiceNotFound:
        raise web_exc.ObjectDoesNotExistsError()
    return ServiceResponse.model_validate(service, from_attributes=True)

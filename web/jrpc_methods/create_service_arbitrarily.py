from common.schemas.service import ServiceCreateRequest, ServiceResponse
from services.service import interactor as service_interactor

from ._rpc_server import entrypoint


@entrypoint.method()
async def create_service(service: ServiceCreateRequest) -> ServiceResponse:
    created_service = await service_interactor.create_service(
        name=service.name,
        description=service.description,
    )
    return ServiceResponse.model_validate(created_service, from_attributes=True)

from common.schemas.service import ArbitrarilyCreateServiceRequest, ServiceResponse
from services.service import interactor as service_interactor

from ._rpc_server import entrypoint


@entrypoint.method(tags=['SERVICE'])
async def create_service_arbitrarily(service: ArbitrarilyCreateServiceRequest) -> ServiceResponse:
    created_service = await service_interactor.create_service(
        name=service.name, description=service.description, requirements=service.requirements
    )
    return ServiceResponse.model_validate(created_service, from_attributes=True)

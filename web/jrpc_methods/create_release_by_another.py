from common.schemas.release import CreateReleaseFromAnother, ReleaseResponse
from services import exceptions as service_exc
from services.releases import interactor as release_interactor
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['RELEASE'],
)
async def create_release_by_another(release: CreateReleaseFromAnother) -> ReleaseResponse:
    try:
        service = await release_interactor.create_release_from_another(
            name=release.name,
            service_id=release.service_id,
            semantic_version=release.semantic_version,
            source_release_id=release.source_release_id,
        )
    except (service_exc.ServiceNotFound, service_exc.ReleaseNotFound):
        raise web_exc.ObjectDoesNotExistsError()
    return ReleaseResponse.model_validate(service, from_attributes=True)

from common.schemas.batch import BatchQuery
from common.schemas.template import TemplatesResponse
from services.template import selectors as template_selectors

from ._rpc_server import entrypoint


@entrypoint.method()
async def get_template_list(batch: BatchQuery) -> TemplatesResponse:
    templates = await template_selectors.select_templates(limit=batch.limit, offset=batch.offset)
    return TemplatesResponse.model_validate(obj=templates, from_attributes=True)

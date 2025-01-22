import uuid

import pydantic


class ReleasePageResponse(pydantic.BaseModel):
    service_space_id: uuid.UUID
    release_id: uuid.UUID
    page_id: str
    webui_link: str

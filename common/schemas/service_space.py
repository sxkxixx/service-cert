import uuid

import pydantic


class ServiceSpace(pydantic.BaseModel):
    id: uuid.UUID
    service_id: uuid.UUID
    webui_link: str
    homepage_id: str | None
    release_folder_id: str | None
    ext_id: str | None
    key: str | None
    alias: str | None

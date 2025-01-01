import uuid

import pydantic


class ReleaseResponse(pydantic.BaseModel):
    id: uuid.UUID
    service_id: uuid.UUID
    name: str
    semantic_version: str | None


class ReleasesResponse(pydantic.RootModel):
    root: list[ReleaseResponse]

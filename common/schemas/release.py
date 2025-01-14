import uuid

import pydantic

from common.schemas.requirement import Requirement


class ReleaseResponse(pydantic.BaseModel):
    id: uuid.UUID
    service_id: uuid.UUID
    name: str
    semantic_version: str | None
    release_requirements: list[Requirement] = pydantic.Field(serialization_alias='requirements')


class ReleaseListResponse(pydantic.BaseModel):
    id: uuid.UUID
    service_id: uuid.UUID
    name: str
    semantic_version: str | None


class ReleasesResponse(pydantic.RootModel):
    root: list[ReleaseListResponse]


class CreateReleaseFromAnother(pydantic.BaseModel):
    name: str
    service_id: uuid.UUID
    semantic_version: str | None
    source_release_id: uuid.UUID

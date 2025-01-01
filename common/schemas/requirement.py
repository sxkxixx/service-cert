import typing
import uuid

import pydantic


class RequirementCreate(pydantic.BaseModel):
    name: str
    value: typing.Any | None = None


class Requirement(RequirementCreate):
    id: uuid.UUID

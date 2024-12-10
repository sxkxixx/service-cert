import uuid

import pydantic

from .requirement import Requirement


class TemplateSchema(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    requirements: list[Requirement]


class TemplatesResponse(pydantic.RootModel):
    root: list[TemplateSchema]

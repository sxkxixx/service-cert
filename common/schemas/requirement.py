import uuid

import pydantic


class Requirement(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    value: str

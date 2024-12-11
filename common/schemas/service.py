import uuid

import pydantic


class ServiceResponse(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    confluence_page_link: str | None


class ServicesResponse(pydantic.RootModel):
    root: list[ServiceResponse]

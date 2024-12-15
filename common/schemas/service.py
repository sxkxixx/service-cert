import uuid

import pydantic


class ServiceCreateRequest(pydantic.BaseModel):
    name: str
    description: str | None


class ServiceResponse(ServiceCreateRequest):
    id: uuid.UUID
    confluence_page_link: str | None


class ServicesResponse(pydantic.RootModel):
    root: list[ServiceResponse]

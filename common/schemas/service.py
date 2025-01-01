import uuid

import pydantic


class ArbitrarilyCreateServiceRequest(pydantic.BaseModel):
    name: str
    description: str | None
    requirements: list[uuid.UUID] = []


class ServiceCreateRequest(pydantic.BaseModel):
    name: str
    description: str | None


class ServiceResponse(ServiceCreateRequest):
    id: uuid.UUID
    confluence_page_link: str | None


class ServicesResponse(pydantic.RootModel):
    root: list[ServiceResponse]

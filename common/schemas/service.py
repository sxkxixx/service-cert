import uuid

import pydantic

from common.schemas.requirement import Requirement, RequirementCreate
from common.schemas.team import Teammate


class CreateServiceFromAnother(pydantic.BaseModel):
    name: str
    description: str | None
    source_service_id: uuid.UUID


class ArbitrarilyCreateServiceRequest(pydantic.BaseModel):
    name: str
    description: str | None
    requirements: list[RequirementCreate] = []


class ServiceCreateRequest(pydantic.BaseModel):
    name: str
    description: str | None
    requirements: list


class ServiceResponse(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    confluence_page_link: str | None
    service_requirements: list[Requirement] = pydantic.Field(serialization_alias='requirements')


class ServiceWithTeam(ServiceResponse):
    team: list[Teammate]


class ServiceListResponse(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    confluence_page_link: str | None


class ServicesResponse(pydantic.RootModel):
    root: list[ServiceListResponse]

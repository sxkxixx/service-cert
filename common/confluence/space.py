import os

from common import db
from common.schemas.space import ConfluenceSpaceResponse
from infrastructure import context

KEY_ALIAS_LENGTH = 16


async def create_service_space(service: db.Service) -> ConfluenceSpaceResponse:
    confluence_client = context.confluence_client.get()
    key_alias = os.urandom(KEY_ALIAS_LENGTH).hex()
    response = await confluence_client.create_space(
        name=service.name,
        key=key_alias,
        alias=key_alias,
        description={
            'plain': {
                'value': service.description or '',
                'representation': 'plain',
            },
        },
    )
    return ConfluenceSpaceResponse.model_validate(response.json())

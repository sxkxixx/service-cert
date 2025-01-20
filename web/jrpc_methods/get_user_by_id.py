import uuid

import fastapi

from common.schemas.user import UserResponse
from services.user import selectors as users_selectors
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(tags=['USER'])
async def get_user_by_id(id_: uuid.UUID = fastapi.Query(alias='id')) -> UserResponse:
    user = await users_selectors.get_user_by_id(id=id_)
    if user is None:
        raise web_exc.ObjectDoesNotExistsError()
    return UserResponse.model_validate(user, from_attributes=True)

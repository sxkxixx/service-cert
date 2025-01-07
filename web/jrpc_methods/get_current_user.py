import fastapi

from common import db
from common.schemas.user import UserResponse
from web.dependencies.user import get_current_user

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['USER'],
)
async def get_current_user(user: db.User = fastapi.Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        nickname=user.nickname,
        email=user.email,
    )

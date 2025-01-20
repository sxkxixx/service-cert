from common.schemas.user import UsersListResponse
from services.user import selectors as user_selectors

from ._rpc_server import entrypoint


@entrypoint.method()
async def get_all_users() -> UsersListResponse:
    users = await user_selectors.get_all()
    return UsersListResponse.model_validate(users, from_attributes=True)

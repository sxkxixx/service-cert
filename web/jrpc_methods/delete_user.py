import fastapi

from services.user import interactor as user_interactor
from web.dependencies.user import get_current_user

from ._rpc_server import entrypoint


@entrypoint.method()
async def delete_user(
    response: fastapi.Response,
    user=fastapi.Depends(get_current_user),
) -> None:
    await user_interactor.delete_user(user_id=user.id)
    response.delete_cookie('refresh_token', path='/api/v1', httponly=True)
    return

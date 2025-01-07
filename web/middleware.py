import fastapi

from common.jwt import AccessToken
from common.utils import request_id
from infrastructure import context
from services.user.selectors import assert_user_exists


async def process_context(request: fastapi.Request, call_next):
    await _set_x_request_id(request=request)
    await _set_context_method(request=request)
    await _set_context_user_id(request=request)

    return await call_next(request)


async def _set_x_request_id(request: fastapi.Request) -> None:
    context.x_request_id.set(request.headers.get('x-request-id', request_id()))


async def _set_context_method(request: fastapi.Request) -> None:
    body = await request.json()
    context.x_request_id.set(body.get('method', None))


async def _set_context_user_id(request: fastapi.Request) -> None:
    authorization_header = 'Authorization'
    access_token_value = request.headers.get(authorization_header, None)
    if access_token_value is None:
        context.user_id.set(None)
        return
    access_token = AccessToken.decode(token=access_token_value)
    user_id = access_token.payload.get('id')
    context.user_id.set(user_id)

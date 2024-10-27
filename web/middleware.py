import typing
from infrastructure import context
from common import utils

from aiohttp import web


@web.middleware
async def set_context(request: web.Request, handler: typing.Callable) -> typing.Any:
    context.x_request_id.set(request.headers.get('x-request-id', utils.refer()))
    return await handler(request)

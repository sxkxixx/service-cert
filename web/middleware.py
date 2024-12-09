import typing

import pydantic
from aiohttp import web

from common import utils
from infrastructure import context


@web.middleware
async def set_context(request: web.Request, handler: typing.Callable) -> typing.Any:
    context.x_request_id.set(request.headers.get('x-request-id', utils.request_id()))
    return await handler(request)


@web.middleware
async def handle_pydantic_validation_error(
    request: web.Request, handler: typing.Callable
) -> typing.Any:
    try:
        return await handler(request)
    except pydantic.ValidationError as exc:
        # TODO: Придумать ошибку
        print(exc)
        pass

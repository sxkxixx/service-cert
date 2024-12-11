from aiohttp import web

from ._rpc_server import rpc_server
from .get_services import get_services
from .get_template_list import get_template_list
from .search_releases import search_releases


async def entrypoint(request: web.Request) -> web.Response:
    request_body = await request.text()
    response = await rpc_server.process_request_async(request_body)
    return web.Response(body=response, content_type='application/json')

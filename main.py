import asyncio

import fastapi_jsonrpc as jsonrpc
import uvicorn
import uvloop
from fastapi.middleware.cors import CORSMiddleware

from common import clients
from infrastructure import context
from infrastructure.config import app_config
from infrastructure.logging import setup_logging
from jobs.main import run_background_tasks
from web import middleware
from web.jrpc_methods import entrypoint


def setup_contextvars() -> None:
    context.confluence_client.set(
        clients.ConfluenceClient(
            base_url=app_config.CONFLUENCE_URL,
            email=app_config.CONFLUENCE_USER_EMAIL,
            api_token=app_config.CONFLUENCE_API_TOKEN,
        ),
    )


def build_application() -> jsonrpc.API:
    setup_logging()
    setup_contextvars()

    application = jsonrpc.API()
    application.bind_entrypoint(ep=entrypoint)
    application.middleware('http')(middleware.process_context)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    return application


app = build_application()

if __name__ == '__main__':
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_background_tasks())
    uvicorn.run(app)

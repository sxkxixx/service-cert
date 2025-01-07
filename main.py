import fastapi_jsonrpc as jsonrpc
import uvicorn
import uvloop

from infrastructure.logging import setup_logging
from web import middleware
from web.jrpc_methods import entrypoint


def build_application() -> jsonrpc.API:
    setup_logging()

    application = jsonrpc.API()
    application.bind_entrypoint(ep=entrypoint)
    application.middleware('http')(middleware.process_context)
    return application


app = build_application()

if __name__ == '__main__':
    uvloop.install()
    uvicorn.run(app)

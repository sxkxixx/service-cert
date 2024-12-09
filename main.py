import uvloop
from aiohttp import web

from infrastructure.logging import setup_logging
from web import middleware
from web.jrpc_methods import entrypoint


def build_application() -> web.Application:
    setup_logging()

    application = web.Application(
        middlewares=[
            middleware.set_context,
            middleware.handle_pydantic_validation_error,
        ],
    )
    application.add_routes(
        [
            web.post('/api/v1', entrypoint),
        ],
    )

    return application


if __name__ == '__main__':
    uvloop.install()
    app = build_application()
    web.run_app(app=app)

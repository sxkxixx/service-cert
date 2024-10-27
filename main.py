import uvloop
from aiohttp import web
from infrastructure.logging import setup_logging
from web import middleware


def init():
    uvloop.install()
    setup_logging()

    application = web.Application(middlewares=[middleware.set_context])

    web.run_app(application)


if __name__ == '__main__':
    init()

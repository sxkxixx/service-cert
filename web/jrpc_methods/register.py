from common import schemas

from ._rpc_server import entrypoint


@entrypoint.method()
async def register(data: schemas.user.AuthUser) -> ...:
    pass

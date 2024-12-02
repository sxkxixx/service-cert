from common import schemas
from ._rpc_server import rpc_server


@rpc_server.method()
async def register(data: schemas.user.AuthUser) -> ...:
    pass

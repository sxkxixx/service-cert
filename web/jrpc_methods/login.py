from common import schemas

from ._rpc_server import rpc_server


@rpc_server.method()
async def login(user: schemas.user.AuthUser):
    pass

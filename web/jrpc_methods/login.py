from common import schemas

from ._rpc_server import entrypoint


@entrypoint.method()
async def login(user: schemas.user.AuthUser):
    pass

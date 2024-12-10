from ._rpc_server import rpc_server


@rpc_server.method()
async def create_project():
    pass

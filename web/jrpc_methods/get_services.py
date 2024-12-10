from ._rpc_server import rpc_server


@rpc_server.method()
async def get_services():
    pass

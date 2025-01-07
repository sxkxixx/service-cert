from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['USER'],
)
async def update_user(update_data: ...) -> None:
    pass

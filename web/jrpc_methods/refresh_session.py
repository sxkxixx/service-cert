import fastapi

from ._rpc_server import entrypoint


@entrypoint.method(description='Метод для обновления сессии')
async def refresh_session(request: fastapi.Request) -> None:
    refresh_token_id = request.cookies.get('refresh_token', None)
    if refresh_token_id is None:
        raise
    _refresh_session = ...

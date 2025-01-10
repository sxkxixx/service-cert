import typing
import uuid
from functools import partial

import pytest
from httpx import ASGITransport, AsyncClient

from main import build_application


@pytest.fixture()
async def test_client() -> AsyncClient:
    app = build_application()
    client = AsyncClient(transport=ASGITransport(app=app), base_url='http://test')
    yield client


def rpc_request_body(method: str, params: dict | None) -> dict:
    return {'jsonrpc': '2.0', 'id': str(uuid.uuid4()), 'method': method, 'params': params or {}}


class JSONRPCResponse(dict):
    @property
    def result(self):
        return self['result']

    @property
    def success(self):
        return 'result' in self and 'error' not in self

    @property
    def failed(self):
        return 'error' in self

    @property
    def error(self):
        return self['error']


@pytest.fixture()
def jrpc_client(test_client: AsyncClient) -> typing.Callable:
    async def _jrpc_request(
        *,
        method: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> JSONRPCResponse:
        data = rpc_request_body(method=method, params=params)
        response = await test_client.post(
            url='/api/v1',
            json=data,
            headers=headers,
        )
        return JSONRPCResponse(**response.json())

    return _jrpc_request


@pytest.fixture()
def authorized_jrpc_client(jrpc_client, access_token: str) -> typing.Callable:
    return partial(jrpc_client, headers={'X-Service-Cert-Id': access_token})

import typing
import uuid

import pytest
from aiohttp.test_utils import TestClient

from main import build_application


@pytest.fixture()
async def test_client(aiohttp_client) -> TestClient:
    app = build_application()
    client = await aiohttp_client(app)
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
def jrpc_client(test_client: TestClient) -> typing.Callable:
    async def _jrpc_request(
        *,
        method: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> JSONRPCResponse:
        data = rpc_request_body(method=method, params=params)
        response = await test_client.post(
            path='/api/v1',
            json=data,
            headers=headers,
        )
        json = await response.json()
        return JSONRPCResponse(**json)

    return _jrpc_request

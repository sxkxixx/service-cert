import asyncio

import pytest


@pytest.fixture(scope="session", autouse=True)
def event_loop(request: pytest.FixtureRequest) -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

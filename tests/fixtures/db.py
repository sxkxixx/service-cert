import pytest

from common.db import async_engine, session_factory


@pytest.fixture(scope='session')
async def db_engine():
    yield async_engine
    await async_engine.dispose()


@pytest.fixture(scope='session')
async def db_connection(db_engine):
    async with db_engine.connect() as conn:
        session_factory.configure(bind=conn, expire_on_commit=False)
        yield conn


@pytest.fixture
async def db_session(db_connection):
    transaction = await db_connection.begin()
    async with session_factory() as session:
        yield session
    await transaction.rollback()

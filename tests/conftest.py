import pytest
import sqlalchemy.event
from sqlalchemy.ext.asyncio import AsyncSession

from common.db.base import async_engine, Base


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield


@pytest.fixture
async def session():
    connection = async_engine.connect()
    transaction = connection.begin()
    session = AsyncSession(bind=connection)

    nested = connection.begin_nested()

    @sqlalchemy.event.listens_for(session, 'after_transaction_end')
    def end_savepoint():
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    await session.close()
    transaction.rollback()
    connection.close()

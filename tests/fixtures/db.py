import pytest
from sqlalchemy.event import listens_for
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncTransaction
from sqlalchemy.orm import Session

from common import db


@pytest.fixture(scope='session')
async def db_engine() -> AsyncEngine:
    yield db.async_engine
    await db.async_engine.dispose()


@pytest.fixture(scope='session')
async def _db_connection(db_engine: AsyncEngine) -> AsyncConnection:
    async with db_engine.connect() as conn:
        db.AsyncSession.configure(bind=conn)
        yield conn


@pytest.fixture(scope='function', autouse=True)
async def db_connection(_db_connection: AsyncConnection) -> AsyncConnection:
    if _db_connection.in_transaction():
        transaction: AsyncTransaction = _db_connection.get_transaction()
    else:
        transaction: AsyncTransaction = await _db_connection.begin()

    savepoint: AsyncTransaction = await _db_connection.begin_nested()

    @listens_for(Session, 'after_transaction_end')
    def on_transaction_end(*args, **kwargs):
        nonlocal savepoint
        if not savepoint.is_active:
            savepoint = _db_connection.sync_connection.begin_nested()

    yield _db_connection
    await transaction.rollback()

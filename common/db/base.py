import contextlib
import logging
import uuid
from datetime import datetime
from typing import AsyncIterator

from sqlalchemy import TIMESTAMP, MetaData, func
from sqlalchemy.ext import asyncio
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from infrastructure.config import app_config

metadata = MetaData()

logger = logging.getLogger(__name__)


class TimestampMixin:
    @declared_attr
    def created_at(self) -> Mapped[datetime]:
        return mapped_column(TIMESTAMP(timezone=True), default=datetime.now)

    @declared_attr
    def updated_at(self) -> Mapped[datetime]:
        if hasattr(self, '_sa_apply_dc_transforms'):
            return mapped_column(
                TIMESTAMP(timezone=True), server_onupdate=func.now(), default=datetime.now
            )


class BaseModel(DeclarativeBase, TimestampMixin):
    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


async_engine = asyncio.create_async_engine(
    url=app_config.db.dsn,
    echo=app_config.db.echo,
    future=True,
)

AsyncSession = asyncio.async_sessionmaker(async_engine, expire_on_commit=False)


@contextlib.asynccontextmanager
async def transaction() -> AsyncIterator[asyncio.AsyncSession]:
    async with AsyncSession() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            logger.exception('Transaction rollback')
            raise
        else:
            logger.debug('Transaction commit')
            await session.commit()

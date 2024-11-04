from datetime import datetime

from sqlalchemy import MetaData, TIMESTAMP, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from infrastructure.config import app_config

metadata = MetaData()


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


class Base(DeclarativeBase, TimestampMixin):
    metadata = metadata


async_engine = create_async_engine(
    url=app_config.db.dsn,
    echo=app_config.db.echo,
)

session = async_sessionmaker(async_engine, expire_on_commit=False)

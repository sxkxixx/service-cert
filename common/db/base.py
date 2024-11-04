from datetime import datetime

from sqlalchemy import MetaData, TIMESTAMP, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

metadata = MetaData()


class TimestampMixin:
    @declared_attr
    def created_at(self) -> Mapped[datetime]:
        if hasattr(
            self, '_sa_apply_dc_transforms'
        ):  # проверка, является ли наследником MappedAsDataclass
            return mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), init=False)
        return mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    @declared_attr
    def updated_at(self) -> Mapped[datetime]:
        if hasattr(
            self, '_sa_apply_dc_transforms'
        ):  # проверка, является ли наследником MappedAsDataclass
            return mapped_column(
                TIMESTAMP(timezone=True),
                server_onupdate=func.now(),
                server_default=func.now(),
                init=False,
            )
        return mapped_column(
            TIMESTAMP(timezone=True), server_onupdate=func.now(), server_default=func.now()
        )


class Base(DeclarativeBase, TimestampMixin):
    metadata = metadata


async_engine = create_async_engine(...)

session = async_sessionmaker(async_engine, expire_on_commit=False)

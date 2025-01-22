import typing
import uuid

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db.base import BaseModel

if typing.TYPE_CHECKING:
    from common.db.models.release import Release
    from common.db.models.service import Service


class ServiceSpace(BaseModel):
    __tablename__ = 'service_space'

    service_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('service.id'),
        nullable=False,
        unique=True,
    )
    webui_link: Mapped[str] = mapped_column(
        sqlalchemy.String(length=128),
        nullable=False,
    )
    homepage_id: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    release_folder_id: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True)
    ext_id: Mapped[str] = mapped_column(
        sqlalchemy.String(length=64),
        nullable=False,
        unique=True,
        index=True,
    )
    key: Mapped[str | None] = mapped_column(
        sqlalchemy.String(length=512),
        nullable=True,
    )
    alias: Mapped[str | None] = mapped_column(
        sqlalchemy.String(length=512),
        nullable=True,
    )

    service: Mapped['Service'] = relationship('Service', back_populates='service_space')
    release_pages: Mapped[list['ReleasePage']] = relationship(
        'ReleasePage', back_populates='service_space'
    )


class ReleasePage(BaseModel):
    __tablename__ = 'release_page'

    service_space_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('service_space.id'),
        nullable=False,
    )
    release_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('release.id'),
        nullable=False,
    )
    page_id: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    webui_link: Mapped[str] = mapped_column(sqlalchemy.String(length=128), nullable=False)

    service_space: Mapped['ServiceSpace'] = relationship(
        'ServiceSpace', back_populates='release_pages'
    )
    release: Mapped['Release'] = relationship('Release', back_populates='release_page')

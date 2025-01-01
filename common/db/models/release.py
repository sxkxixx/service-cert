import typing
import uuid

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import base

if typing.TYPE_CHECKING:
    from common.db.models.requirements import ReleaseRequirement
    from common.db.models.service import Service


class Release(base.BaseModel):
    __tablename__ = 'release'

    service_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('service.id'),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(sqlalchemy.String(length=128), nullable=False)
    semantic_version: Mapped[str] = mapped_column(sqlalchemy.String(length=32), nullable=True)

    service: Mapped['Service'] = relationship(
        'Service',
        back_populates='releases',
    )
    release_requirements: Mapped[list['ReleaseRequirement']] = relationship(
        'ReleaseRequirement',
        back_populates='release',
    )

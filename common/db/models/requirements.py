import typing
import uuid

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import base

if typing.TYPE_CHECKING:
    from common.db.models.release import Release
    from common.db.models.service import Service


class _Requirement:
    name: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    value: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True)


class ServiceRequirement(base.BaseModel, _Requirement):
    __tablename__ = 'service_requirement'

    service_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('service.id'), nullable=False
    )
    service: Mapped['Service'] = relationship('Service', back_populates='service_requirements')


class ReleaseRequirement(base.BaseModel, _Requirement):
    __tablename__ = 'release_requirement'

    release_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('release.id'), nullable=False
    )
    release: Mapped['Release'] = relationship('Release', back_populates='release_requirements')

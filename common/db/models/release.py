import typing
import uuid

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import base

if typing.TYPE_CHECKING:
    from common.db.models.service import Service
    from common.db.models.template import Template


class Release(base.BaseModel):
    __tablename__ = 'release'

    service_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('service.id'),
        nullable=False,
    )
    template_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('template.id'),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(sqlalchemy.String(length=128), nullable=False)
    semantic_version: Mapped[str] = mapped_column(sqlalchemy.String(length=32), nullable=True)

    service: Mapped['Service'] = relationship('Service', back_populates='releases')
    template: Mapped['Template'] = relationship('Template', back_populates='releases')

import typing

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import base

if typing.TYPE_CHECKING:
    from common.db.models.release import Release
    from common.db.models.requirements import ServiceRequirement
    from common.db.models.team import Teammate


class Service(base.BaseModel):
    __tablename__ = 'service'

    name: Mapped[str] = mapped_column(sqlalchemy.String(length=128), nullable=False)
    description: Mapped[str | None] = mapped_column(sqlalchemy.String(length=512), nullable=True)
    confluence_page_link: Mapped[str | None] = mapped_column(
        sqlalchemy.String(length=64),
        nullable=True,
    )

    releases: Mapped[list['Release']] = relationship('Release', back_populates='service')
    service_requirements: Mapped[list['ServiceRequirement']] = relationship(
        'ServiceRequirement',
        back_populates='service',
    )
    team: Mapped[list['Teammate']] = relationship('Teammate', back_populates='service')

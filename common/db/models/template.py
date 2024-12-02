import typing
import uuid

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import base

if typing.TYPE_CHECKING:
    from common.db.models.release import Release


class Template(base.BaseModel):
    __tablename__ = "template"

    name: Mapped[str] = mapped_column(sqlalchemy.String(length=128), nullable=False)

    releases: Mapped['Release'] = relationship('Release', back_populates='template')
    requirements: Mapped[list["Requirement"]] = relationship(
        secondary="template__requirement_association",
        back_populates="templates"
    )
    requirement_associations: Mapped[list["TemplateRequirementAssociation"]] = relationship(
        back_populates="template"
    )


class TemplateRequirementAssociation(base.BaseModel):
    __tablename__ = "template__requirement_association"

    template_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('template.id'), nullable=False,
    )
    requirement_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('requirement.id'), nullable=False,
    )

    requirement: Mapped["Requirement"] = relationship(back_populates="template_associations")
    template: Mapped["Template"] = relationship(back_populates="requirement_associations")


class Requirement(base.BaseModel):
    __tablename__ = "requirement"

    name: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True)
    value: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(sqlalchemy.Boolean(), nullable=False, default=False)

    templates: Mapped[list["Template"]] = relationship(
        secondary="template__requirement_association",
        back_populates="requirements",
    )
    template_associations: Mapped[list["TemplateRequirementAssociation"]] = relationship(
        back_populates="requirement",
    )

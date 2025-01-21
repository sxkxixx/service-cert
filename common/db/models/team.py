import typing
import uuid

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db.base import BaseModel

if typing.TYPE_CHECKING:
    from common.db.models.service import Service
    from common.db.models.user import User


class Teammate(BaseModel):
    __tablename__ = 'teammate'

    user_id: Mapped[uuid.UUID] = mapped_column(sqlalchemy.ForeignKey('user.id'), nullable=False)
    service_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.ForeignKey('service.id'), nullable=False
    )

    user: Mapped['User'] = relationship('User')
    service: Mapped['Service'] = relationship('Service', back_populates='team')

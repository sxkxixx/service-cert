import datetime
import uuid

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db.base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    first_name: Mapped[str] = mapped_column(sqlalchemy.String(length=32), nullable=False)
    last_name: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    email: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(sqlalchemy.String(length=512), nullable=False)

    refresh_session: Mapped['RefreshSession'] = relationship('RefreshSession', back_populates='user')


class RefreshSession(BaseModel):
    __tablename__ = 'refresh_session'

    user_id: Mapped[uuid.UUID] = mapped_column(sqlalchemy.ForeignKey('user.id'), nullable=False, unique=True)
    expired_in: Mapped[datetime.datetime] = mapped_column(sqlalchemy.DateTime(timezone=False), nullable=False)
    """UTC"""
    refresh_token: Mapped[str] = mapped_column(sqlalchemy.String(length=512), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='refresh_session')

    def is_expired(self) -> bool:
        return self.expired_in < datetime.datetime.utcnow()

import datetime
import uuid

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db.base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    first_name: Mapped[str] = mapped_column(sqlalchemy.String(length=32), nullable=False)
    last_name: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    email: Mapped[str] = mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(sqlalchemy.String(length=512), nullable=False)

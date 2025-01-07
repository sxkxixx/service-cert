import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

from common.db.base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(sqlalchemy.String(length=128), nullable=False)
    nickname: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    email: Mapped[str] = mapped_column(
        sqlalchemy.String(length=64),
        nullable=False,
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column(sqlalchemy.String(length=512), nullable=False)

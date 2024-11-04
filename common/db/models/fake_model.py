import uuid
from uuid import UUID

from common.db.base import Base
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column
from sqlalchemy import String


class FakeModel(MappedAsDataclass, Base):
    __tablename__ = 'fake_model'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4, init=False)
    column: Mapped[str] = mapped_column(String(length=64))

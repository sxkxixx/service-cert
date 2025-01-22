import uuid

import sqlalchemy

from common import db


def get_service_space_by_service_id(service_id: uuid.UUID, lock: bool = False) -> sqlalchemy.Select:
    stmt = (
        sqlalchemy.select(db.ServiceSpace).where(db.ServiceSpace.service_id == service_id).limit(1)
    )
    if lock:
        return stmt.with_for_update()
    return stmt

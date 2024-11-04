import sqlalchemy

from common.db.base import session
from common.db.models.fake_model import FakeModel


async def test():
    async with session() as _session:
        statement = (
            sqlalchemy.insert(FakeModel)
            .values(column='11221212121212121212121')
            .returning(FakeModel)
        )
        res = await _session.scalar(statement)
        assert res.column == '11221212121212121212121'

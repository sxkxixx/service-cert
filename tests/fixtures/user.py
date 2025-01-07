import os

import pytest
from polyfactory import AsyncPersistenceProtocol

from common import db, hasher, jwt
from services.user.interactor import get_user_dict

from .factory_mixin import AsyncPersistenceAlchemyMixin, CustomSQLAlchemyFactory


class AsyncUserPersistence(AsyncPersistenceAlchemyMixin, AsyncPersistenceProtocol[db.User]):
    pass


class UserFactory(CustomSQLAlchemyFactory[db.User]):
    __model__ = db.User
    __async_persistence__ = AsyncUserPersistence

    @classmethod
    def password(cls) -> str:
        return hasher.get_password_hash(os.urandom(16).hex())

    @classmethod
    def email(cls) -> str:
        return 'zubenko.mikhail@gmail.com'


@pytest.fixture
async def user() -> db.User:
    return await UserFactory.create_async()


@pytest.fixture
async def user_with_pwd() -> db.User:
    return await UserFactory.create_async(password=hasher.get_password_hash('mafia'))


@pytest.fixture()
async def access_token(user: db.User) -> str:
    return jwt.AccessToken(payload=get_user_dict(user)).encode()

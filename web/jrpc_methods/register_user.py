import sqlalchemy.exc

from common.schemas.user import RegisterUser, UserResponse
from services import user as user_service
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['USER'],
    description='Метод для регистрации пользователя в сервисе',
    errors=[web_exc.AlreadyExistsError],
)
async def register_user(data: RegisterUser) -> UserResponse:
    try:
        user = await user_service.interactor.create_user(
            name=data.name,
            nickname=data.nickname,
            email=data.email,
            password=data.password,
        )
    except sqlalchemy.exc.IntegrityError:
        raise web_exc.AlreadyExistsError()
    return UserResponse.model_validate(user, from_attributes=True)

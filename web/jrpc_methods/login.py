import fastapi

from common import hasher, jwt, schemas
from services import user as user_service
from web import exceptions as web_exc

from ._rpc_server import entrypoint


@entrypoint.method(
    tags=['AUTH'],
    errors=[web_exc.AuthenticationError],
)
async def login(login_data: schemas.user.UserLoginRequest, response: fastapi.Response) -> dict:
    user = await user_service.selectors.get_user_by_email_or_nickname(
        factor=login_data.first_factor
    )
    if user is None:
        raise web_exc.AuthenticationError()
    if not hasher.verify_password(plain_password=login_data.password, hash_password=user.password):
        raise web_exc.AuthenticationError()
    payload = user_service.interactor.get_user_dict(user=user)
    access_token = jwt.AccessToken(payload=payload.copy()).encode()
    response.headers['X-Service-Cert-Id'] = access_token
    return {'access_token': access_token}

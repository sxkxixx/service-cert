from common import db
from infrastructure import context
from services.user.selectors import get_user_by_id
from web import exceptions as web_exc


async def get_current_user() -> db.User:
    user = await get_user_by_id(id=context.user_id.get())
    if user is None:
        raise web_exc.AuthenticationError()
    return user

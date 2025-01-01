import datetime

import pydantic
from jose import jwt

from infrastructure.config import app_config


class TokenPayload(pydantic.BaseModel):
    payload: dict
    time_to_leave: datetime.timedelta = None

    def encode(self) -> str:
        self.payload['exp'] = self.expires_in
        return jwt.encode(claims=self.payload, key=app_config.SECRET_KEY)

    @classmethod
    def decode(cls, token) -> 'TokenPayload':
        payload = jwt.decode(token=token, key=app_config.SECRET_KEY)
        return TokenPayload(payload=payload)

    @property
    def expires_in(self) -> datetime.datetime:
        return datetime.datetime.now() + self.time_to_leave

    def __str__(self) -> str:
        return self.encode()


class AccessToken(TokenPayload):
    time_to_leave: datetime.timedelta = app_config.access_token_timedelta


class RefreshToken(TokenPayload):
    time_to_leave: datetime.timedelta = app_config.refresh_token_timedelta

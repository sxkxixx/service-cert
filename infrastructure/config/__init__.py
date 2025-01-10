import datetime

import pydantic
import pydantic_settings

__all__ = [
    'app_config',
]


class _ApplicationConfig(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    POSTGRES_USER: str = 'service_cert'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str = 'service_cert'
    POSTGRES_PASSWORD: str = 'service_cert'
    POSTGRES_PORT: int = 5432
    echo: bool = False

    SECRET_KEY: str = ''
    ACCESS_TOKEN_MINUTES_TTL: int = 5
    REFRESH_TOKEN_DAYS_TTL: int = 5

    # CONFLUENCE
    CONFLUENCE_URL: str = ''
    CONFLUENCE_USER_EMAIL: str = ''
    CONFLUENCE_API_TOKEN: str = ''

    # Background Tasks Period
    BACKGROUND_TASK_PERIOD: int | None = pydantic.Field(default=None)

    @pydantic.computed_field()
    @property
    def dsn(self) -> str:
        return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'.format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            db_name=self.POSTGRES_DB,
        )

    @pydantic.computed_field()
    @property
    def access_token_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(minutes=self.ACCESS_TOKEN_MINUTES_TTL)

    @pydantic.computed_field()
    @property
    def refresh_token_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(minutes=self.REFRESH_TOKEN_DAYS_TTL)


app_config = _ApplicationConfig()

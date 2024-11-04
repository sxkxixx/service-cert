from pydantic_settings import BaseSettings

from ._db import DatabaseConfig

__all__ = [
    'app_config',
]


class _ApplicationConfig(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()


app_config = _ApplicationConfig()

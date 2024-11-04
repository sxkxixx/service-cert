from pydantic import BaseModel, computed_field


class DatabaseConfig(BaseModel):
    POSTGRES_USER: str = 'service_cert'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str = 'service_cert'
    POSTGRES_PASSWORD: str = 'service_cert'
    POSTGRES_PORT: int = 5432
    echo: bool = False

    @computed_field
    @property
    def dsn(self) -> str:
        return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'.format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            db_name=self.POSTGRES_DB,
        )

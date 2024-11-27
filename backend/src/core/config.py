import secrets
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith('['):
        return [i.strip() for i in v.split(',')]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_ignore_empty=True, extra='ignore')
    PROJECT_NAME: str
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)

    DOMAIN: str = 'localhost'
    ENVIRONMENT: Literal['local', 'staging', 'production'] = 'local'
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    # Neo4j connection parameters
    NEO4J_HOST: str = 'localhost'
    NEO4J_PORT: int = 7687
    NEO4J_USER: str = 'neo4j'
    NEO4J_PASSWORD: str = ''

    @computed_field  # type: ignore[misc]
    @property
    def DATABASE_URL(self) -> str:
        return f'bolt://{self.NEO4J_USER}:{self.NEO4J_PASSWORD}@{self.NEO4J_HOST}:{self.NEO4J_PORT}'

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == 'local':
            return f'http://{self.DOMAIN}'
        return f'https://{self.DOMAIN}'


settings = Settings()  # type: ignore

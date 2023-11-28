from functools import lru_cache
from pathlib import Path
from typing import Dict

from dotenv import find_dotenv
from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings
from pydantic.types import SecretStr, PositiveInt

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev`.
    """
    #: str: Postgresql host.
    POSTGRES_HOST: str
    #: PositiveInt: positive int (x > 0) port of postgresql.
    POSTGRES_PORT: PositiveInt
    #: str: Postgresql user.
    POSTGRES_USER: str
    #: SecretStr: Postgresql password.
    POSTGRES_PASSWORD: SecretStr
    #: str: Postgresql database name.
    POSTGRES_DATABASE_NAME: str

    # Static_info: path for download and save img link
    STATIC_PATH: Path
    DOWNLOAD_PATH: str

    # Host info
    HOST_URL: SecretStr
    HOST_PORT: SecretStr
    #: SecretStr: secret x-token for authority.
    X_API_TOKEN_STATIC: SecretStr

    # # Browser info: headers
    # HEADERS: Dict
    #
    # # Img source url
    #
    # URL: str
    # Соль для JWToken
    SECRET_KEY_TOKEN: SecretStr

    @validator("STATIC_PATH")
    def create_static_path(cls, v: Path) -> Path:
        """Create static files directory."""
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))

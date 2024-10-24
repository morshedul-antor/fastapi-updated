from pydantic import AnyHttpUrl, HttpUrl, field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Union
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        os.environ.get("URL_ONE"),
        os.environ.get("URL_TWO"),
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "FastAPI"
    SENTRY_DSN: Optional[HttpUrl] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

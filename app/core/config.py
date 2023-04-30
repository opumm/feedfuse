import secrets
from typing import Any, Dict, Optional

from pydantic import AmqpDsn, BaseSettings, EmailStr, PostgresDsn, RedisDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    TASKIQ_BROKER_URL: AmqpDsn
    TASKIQ_RESULT_BACKEND: str
    CRAWLER_MAX_RETRIES: int = 3
    CRAWLER_RETRY_INTERVAL_SECONDS: int = 10

    WORKER_BROKER_DSN: AmqpDsn = "amqp://guest:guest@rabbitmq:5672"
    WORKER_BACKEND_DSN: RedisDsn = "redis://redis:6379/0"
    SCRAPPER_INTERVAL_SECONDS: int = "15"
    SCRAPPER_MAX_RETRIES: int = "3"
    SCRAPPER_RETRY_INTERVAL_SECONDS: int = 15

    CRAWLER_SCHEDULER_CRON: str = "* * * * *"  # Runs every minute

    FIRST_USER: EmailStr
    FIRST_USER_PASSWORD: str

    class Config:
        case_sensitive = True


settings = Settings()

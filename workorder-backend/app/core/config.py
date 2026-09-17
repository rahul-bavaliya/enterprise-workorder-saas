# app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py is inside app/core/ (3 levels down from your backend root)
# .parent.parent.parent maps exactly to your workorder-backend/ root directory
BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BACKEND_ROOT / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Work-Order SaaS"
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

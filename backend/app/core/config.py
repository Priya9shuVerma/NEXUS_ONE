from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "NEXUS ONE"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # API keys used by AI/LLM integrations. Make optional so the
    # settings loader accepts their presence in .env without failing.
    GROQ_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None

    # Optional legacy JWT secret (kept for compatibility). Set in .env
    # only if you need to accept tokens signed with an older key.
    LEGACY_SECRET: str | None = None

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
"""Application configuration settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Todo API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A modern Todo application API built with FastAPI"

    # Database Settings
    DATABASE_URL: str = "sqlite:///./todos.db"

    # CORS Settings
    CORS_ORIGINS: list = ["*"]

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()

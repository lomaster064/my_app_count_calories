from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://app:app@db:5432/app"
    jwt_secret: str = "devsecret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    cors_origins: str = "*"
    minio_endpoint: str = "http://minio:9000"
    minio_root_user: str = "minio"
    minio_root_password: str = "minio123"
    minio_bucket: str = "meal-photos"
    minio_region: str = "us-east-1"
    openai_api_key: str | None = None
    ai_provider: str = "openai"
    redis_url: str = "redis://redis:6379/0"
    environment: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

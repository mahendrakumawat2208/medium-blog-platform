from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database (use SQLite by default if no .env; set DATABASE_URL for Postgres)
    database_url: str = "sqlite:///./folio.db"

    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # App
    project_name: str = "Folio Blog API"
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

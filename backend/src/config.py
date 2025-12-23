from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra='ignore')

    # Database
    DATABASE_URL: str
    NEON_DATABASE_URL: str | None = None

    # Authentication
    BETTER_AUTH_SECRET: str
    BETTER_AUTH_URL: str = "http://localhost:3000"

    # Backend
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    API_V1_PREFIX: str = "/api/v1"

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def get_database_url(self) -> str:
        """Get the appropriate database URL"""
        return self.NEON_DATABASE_URL if self.NEON_DATABASE_URL else self.DATABASE_URL


settings = Settings()
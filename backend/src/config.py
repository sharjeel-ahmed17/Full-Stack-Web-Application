from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All sensitive data should be stored in .env file (not committed to git).
    See .env.example for required variables.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database Configuration
    # Use DATABASE_URL for the active database connection
    DATABASE_URL: str

    # Optional: Separate production database URL (e.g., Neon)
    NEON_DATABASE_URL: Optional[str] = None

    # Authentication & Security
    # CRITICAL: Must be a strong, random secret key (min 32 characters)
    BETTER_AUTH_SECRET: str
    BETTER_AUTH_URL: Optional[str] = None

    # Backend API Configuration
    BACKEND_CORS_ORIGINS: Optional[str] = None
    API_V1_PREFIX: str = "/api/v1"

    # JWT Token Configuration
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application Environment
    ENVIRONMENT: str = "development"  # development, staging, production

    @property
    def get_database_url(self) -> str:
        """
        Get the appropriate database URL.
        Prioritizes NEON_DATABASE_URL if set, otherwise uses DATABASE_URL.
        """
        return self.NEON_DATABASE_URL if self.NEON_DATABASE_URL else self.DATABASE_URL

    @property
    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        if self.BACKEND_CORS_ORIGINS:
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
        return []


# Initialize settings instance
# This will automatically load from .env file
settings = Settings()
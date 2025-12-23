from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra='ignore')

    # Database
    # DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/todoapp"
    DATABASE_URL: str = "postgresql://neondb_owner:npg_Zjb2M9kBdJKP@ep-misty-moon-a11gvptq-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

    # Authentication
    BETTER_AUTH_SECRET: str = "CSct0S3JwOI6NIZPVSSsXp6nS89VFIsY"
    BETTER_AUTH_URL: str = "http://localhost:3000"

    # Backend
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    API_V1_PREFIX: str = "/api/v1"

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
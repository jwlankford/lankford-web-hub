from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Match the credentials defined in your docker-compose.yml
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "development_password_only"
    POSTGRES_DB: str = "lankford_hub_dev"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        # Construct the async connection string required by asyncpg
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
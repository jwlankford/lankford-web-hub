import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Set USE_SQLITE to True for Docker-free local database operation
    USE_SQLITE: bool = False
    SQLITE_FILE: str = "lankford_hub.db"

    # PostgreSQL configuration
    DATABASE_URL: str | None = None
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "development_password_only"
    POSTGRES_DB: str = "lankford_hub_dev"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    
    # Gemini API configuration
    GEMINI_API_KEY: str | None = None

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        if self.USE_SQLITE:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.SQLITE_FILE)
            return f"sqlite+aiosqlite:///{db_path}"
            
        if self.DATABASE_URL:
            # Inject asyncpg driver for standard postgresql URLs
            url = self.DATABASE_URL
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://")
            
            # Remove unsupported query parameters from asyncpg URL
            if "?" in url:
                url, _ = url.split("?")
                
            return url
            
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
from pydantic_settings import BaseSettings  # ✅ Correct import for Pydantic v2+

class Settings(BaseSettings):
    PROJECT_NAME: str = "Trading Journal API"
    VERSION: str = "1.0"
    DATABASE_URL: str = "sqlite:///./trading_journal.db"  # Update for PostgreSQL if needed
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = "../.env"

settings = Settings()

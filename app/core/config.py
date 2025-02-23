from pydantic_settings import BaseSettings  # ✅ Correct import for Pydantic v2+
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Trading Journal API"
    VERSION: str = "1.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL")  # ✅ Load from .env
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()


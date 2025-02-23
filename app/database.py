from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings



DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)  # ✅ Add connection pooling for PostgreSQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import app.models  # This loads everything inside `app/models/__init__.py`
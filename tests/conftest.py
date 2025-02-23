import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.core.config import settings

# ✅ Use a separate test database
TEST_DATABASE_URL = settings.DATABASE_URL + "_test"

# ✅ Set up the test engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure database schema is created before tests."""
    Base.metadata.drop_all(bind=engine)  # Clear test DB
    Base.metadata.create_all(bind=engine)  # Recreate schema
    yield
    Base.metadata.drop_all(bind=engine)  # Clean up after tests

@pytest.fixture()
def db():
    """Provide a clean database session to each test."""
    session = TestingSessionLocal()
    try:
        yield session
        session.rollback()  # Ensure no leftover data between tests
    finally:
        session.close()

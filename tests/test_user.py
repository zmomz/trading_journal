import pytest
from sqlalchemy.orm import Session
from app.crud.user import create_user, get_user, update_user, soft_delete_user
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.models.trade import Trade
from app.models.note import TradeNote


@pytest.fixture
def test_db_cleanup(db: Session):
    """Ensure clean database state before each test"""
    db.query(TradeNote).delete()  # Delete trade notes first
    db.query(Trade).delete()  # Delete trades next
    db.query(User).delete()  # Now it's safe to delete users
    db.commit()

@pytest.fixture
def test_user(db: Session, test_db_cleanup):
    """Create a test user before inserting any dependent records"""
    user_data = UserCreate(username="testuser", email="test@example.com", password="securepassword")
    return create_user(db, user_data)

def test_create_user(db: Session):
    user_data = UserCreate(
        username="newuser",
        email="new@example.com",
        password="password123"  # Pass plain password
    )
    user = create_user(db, user_data)
    assert user.id is not None
    assert user.email == "new@example.com"

def test_get_user(db: Session, test_user):
    user = get_user(db, test_user.id)
    assert user is not None
    assert user.username == "testuser"

def test_update_user(db: Session, test_user):
    update_data = UserUpdate(
        username="updateduser",
        email="updated@example.com"  # Ensure required fields are provided
    )
    updated_user = update_user(db, test_user.id, update_data)
    assert updated_user.username == "updateduser"
    assert updated_user.email == "updated@example.com"

def test_soft_delete_user(db: Session, test_user):
    soft_delete_user(db, test_user.id)
    deleted_user = get_user(db, test_user.id)
    assert deleted_user is not None  # User still exists in DB
    assert deleted_user.is_active is False  # Ensure it's marked as inactive

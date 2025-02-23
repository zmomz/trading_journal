import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate
from app.core.security import verify_password

def test_create_user(db: Session):
    user_data = UserCreate(username="testuser", email="test@example.com", password="securepassword")
    
    # ✅ Ensure user does not exist before running the test
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        db.delete(existing_user)
        db.commit()
    
    # ✅ Now create the user
    user = create_user(db, user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"

    # ✅ Attempting to create the same user again should raise an IntegrityError
    try:
        create_user(db, user_data)
        assert False, "Creating duplicate user should raise IntegrityError"
    except IntegrityError:
        db.rollback()

def test_get_user_by_email(db: Session):
    email = "test@example.com"
    user = get_user_by_email(db, email)
    assert user is not None
    assert user.email == email

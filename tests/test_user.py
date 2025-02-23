import pytest
from sqlalchemy.orm import Session
from app.models.user import User
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate
from app.core.security import verify_password

def test_create_user(db: Session):
    user_data = UserCreate(username="testuser", email="test@example.com", password="securepassword")
    user = create_user(db, user_data)
    assert user.username == user_data.username
    assert user.email == user_data.email
    assert verify_password("securepassword", user.hashed_password)

def test_get_user_by_email(db: Session):
    email = "test@example.com"
    user = get_user_by_email(db, email)
    assert user is not None
    assert user.email == email

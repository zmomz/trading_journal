from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not db_user:
        return None

    if user_update.username:
        db_user.username = user_update.username
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = pwd_context.hash(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user

def soft_delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not db_user:
        return None

    db_user.is_active = False  # Soft delete by marking inactive
    db.commit()
    db.refresh(db_user)  # Ensure it's refreshed before returning
    return db_user  # Return the updated user
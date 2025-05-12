from sqlalchemy.orm import Session
from backend.app.models import User
from backend.app.schemas import UserCreate, UserUpdate
from backend.app.security import get_password_hash, verify_password
from backend.app import models

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email, full_name=user.full_name, password_hash=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.full_name = user.full_name
        if user.password:
            db_user.password_hash = get_password_hash(user.password)
        db.commit()
        db.refresh(db_user)
    return db_user

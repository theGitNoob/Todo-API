from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.crypto import get_password_hash


def get_user(username: str, db: Session) -> User:
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_items(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user.items


def create_user(db: Session, user: UserCreate):
    hashed_pwd = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

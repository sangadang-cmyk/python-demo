from sqlalchemy.orm import Session

import models
from schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = models.User(displayName=user.displayName, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # reload with generated id
    return db_user

def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db_user.displayName = user.displayName
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
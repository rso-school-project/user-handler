from sqlalchemy.orm import Session

import hashlib

from . import models, schemas

salt = "salt1"

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_username_password(db: Session, user: schemas.UserLogin):
    hashed_password = hashlib.sha1((user.password + salt).encode('utf-8')).hexdigest()
    return db.query(models.User).filter(models.User.username == user.username).filter(models.User.password == hashed_password).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashlib.sha1((user.password + salt).encode('utf-8')).hexdigest()
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

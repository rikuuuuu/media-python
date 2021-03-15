from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, name="", refresh_token="")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, item: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == int(item.id)).first()
    db_user.name = item.name
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, item: schemas.UserDelete):
    db.query(models.User).filter(models.User.id == int(item.id)).delete()
    db.commit()
    return

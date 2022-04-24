from sqlalchemy.orm import Session

import models
import schemas


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_name(name: str, db: Session):
    return db.query(models.User).filter(models.User.name == name).first()

def create_user(user: schemas.UserCreate, db: Session):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(name=user.name, email=user.email, gender=user.gender, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def edit_user(user: schemas.UserCreate, db: Session):
    db_user = db.query(models.User).filter(models.User.name == user.name).first()
    fake_hashed_password = user.password + "notreallyhashed"

    db_user.name= user.name
    db_user.email = user.email
    db_user.gender = user.gender
    db_user.imageUrl = user.imageUrl
    db_user.password = fake_hashed_password

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user: models.User, db: Session):
    db.delete(user)
    db.commit()

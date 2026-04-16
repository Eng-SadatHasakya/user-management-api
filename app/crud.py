from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hash_password
from . import models

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):

    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        return None
    
    new_user = models.User(
        name=user.name, 
        email=user.email, 
        password=hash_password(user.password)   
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def delete_user(db: Session, user):
    db.delete(user)
    db.commit()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
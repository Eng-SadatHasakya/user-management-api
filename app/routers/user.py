from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas  
from .. import models, crud, models
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).filter()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered") 
    
    return crud.create_user(db, user.name, user.email)

@router.get("/users/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") 
      
    crud.delete_user(db, user)
    return{"message": "Deleted"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from ..auth import create_access_token, verify_password
from ..auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = crud.create_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return new_user

@router.get("/users/")
def read_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return crud.get_users(db)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") 
      
    crud.delete_user(db, user)
    return{"message": "Deleted"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

    #Generate and return JWT token
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
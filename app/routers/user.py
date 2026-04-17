from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from ..auth import verify_password, create_access_token, get_current_user, require_admin
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

#Public - anyone can create account
@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = crud.create_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return new_user

#Public -login
@router.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    #Include role in token
    access_token = create_access_token(data={
        "sub": db_user.email,
        "role": db_user.role
    })
    return {"access_token": access_token, "token_type": "bearer"}

#Admin only - get all users
@router.get("/users/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    return crud.get_users(db)

#Any logged in user - get own profile
@router.get("/users/me/", response_model=schemas.UserResponse)
def read_user_me(db: Session  = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.User).filter(models.User.email == current_user["email"]).first()

#Admin only - delete user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") 
      
    crud.delete_user(db, user)
    return{"message": "Deleted"}

    #Generate and return JWT token
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
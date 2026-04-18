from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from ..auth import verify_password, create_access_token, create_refresh_token, is_token_expired, get_current_user, require_admin
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

# Public - anyone can create account
@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    logger.info(f"New user created: {user.email}")  # ✅ inside function
    return new_user

# Public - login
@router.post("/login/")
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={
        "sub": db_user.email,
        "role": db_user.role
    })
    refresh_token = create_refresh_token()
    crud.save_refresh_token(db, db_user.email, refresh_token)
    logger.info(f"User {db_user.email} logged in successfully")  # ✅ inside function
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Admin only - get all users
@router.get("/users/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    return crud.get_users(db)

# Any logged in user - get own profile
@router.get("/users/me/", response_model=schemas.UserResponse)
def read_user_me(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.User).filter(models.User.email == current_user["email"]).first()

# Admin only - delete user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user)
    logger.warning(f"Admin {current_user['email']} deleted user {user_id}")  # ✅ inside function
    return {"message": "Deleted"}

# Refresh access token
@router.post("/refresh/")
def refresh_token(request: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    db_token = crud.get_refresh_token(db, request.refresh_token)
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if is_token_expired(db_token.expires_at):
        crud.delete_refresh_token(db, request.refresh_token)
        raise HTTPException(status_code=401, detail="Refresh token expired, please login again")
    new_access_token = create_access_token(data={"sub": db_token.user_email})
    return {"access_token": new_access_token, "token_type": "bearer"}

# Logout - revoke refresh token
@router.post("/logout/")
def logout(request: schemas.RefreshTokenRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    crud.delete_refresh_token(db, request.refresh_token)
    logger.info(f"User {current_user['email']} logged out")  # ✅ inside function
    return {"message": "Logged out successfully"}

# Logout from all devices
@router.post("/logout-all/")
def logout_all(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    crud.delete_all_user_tokens(db, current_user["email"])
    logger.info(f"User {current_user['email']} logged out from all devices")  # ✅ inside function
    return {"message": "Logged out from all devices"}
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
class UserLogin(BaseModel):
    email: str
    password: str
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str



class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    bio: str | None = None
    profile_image: str | None = None



# -------- Password Change -------- #

class PasswordChange(BaseModel):
    old_password: str
    new_password: str



class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    full_name: str | None = None
    phone: str | None = None
    bio: str | None = None
    profile_image: str | None = None

    is_active: bool
    created_at: datetime


    class Config:
        from_attributes = True
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


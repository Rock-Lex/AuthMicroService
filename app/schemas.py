from pydantic import BaseModel
from typing import Optional
import uuid


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: Optional[str] = None  # Password is optional for third-party users
    third_party_id: Optional[str] = None  # For third-party users (Google/Apple)
    auth_provider: Optional[str] = None  # To specify if the user is registering via Google/Apple

class UserOut(UserBase):
    is_active: bool
    class Config:
        orm_mode = True

class UserOutCreated(BaseModel):
    uuid: uuid.UUID

    class Config:
        orm_mode = True

class LoginForm(BaseModel):
    email: str
    password: str

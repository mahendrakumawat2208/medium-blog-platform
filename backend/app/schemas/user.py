from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserUpdate(BaseModel):
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.user import UserResponse


class PostBase(BaseModel):
    title: str
    body: str
    body_format: str = "markdown"
    cover_image_url: str | None = None


class PostCreate(PostBase):
    published: bool = False


class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    body_format: str | None = None
    cover_image_url: str | None = None
    published: bool | None = None


class PostAuthor(BaseModel):
    id: UUID
    username: str
    display_name: str | None = None
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: UUID
    author_id: UUID
    author: PostAuthor | None = None
    title: str
    slug: str
    body: str
    body_format: str
    cover_image_url: str | None = None
    published_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

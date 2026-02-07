from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user, get_current_user_optional
from app.core.database import get_db
from app.core.slug import slugify
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostAuthor

router = APIRouter(prefix="/posts", tags=["posts"])


def _post_to_response(post: Post) -> PostResponse:
    return PostResponse(
        id=post.id,
        author_id=post.author_id,
        author=PostAuthor(
            id=post.author.id,
            username=post.author.username,
            display_name=post.author.display_name,
            avatar_url=post.author.avatar_url,
        ) if post.author else None,
        title=post.title,
        slug=post.slug,
        body=post.body,
        body_format=post.body_format,
        cover_image_url=post.cover_image_url,
        published_at=post.published_at,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.post("", response_model=PostResponse)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    base_slug = slugify(data.title)
    slug = base_slug
    n = 0
    while db.query(Post).filter(Post.slug == slug).first():
        n += 1
        slug = f"{base_slug}-{n}"
    post = Post(
        author_id=user.id,
        title=data.title,
        slug=slug,
        body=data.body,
        body_format=data.body_format,
        cover_image_url=data.cover_image_url,
        published_at=datetime.utcnow() if data.published else None,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    post = db.query(Post).options(joinedload(Post.author)).filter(Post.id == post.id).first()
    return _post_to_response(post)


@router.get("", response_model=list[PostResponse])
def list_posts(
    author_id: UUID | None = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(Post).options(joinedload(Post.author)).filter(Post.published_at.isnot(None))
    if author_id:
        q = q.filter(Post.author_id == author_id)
    posts = q.order_by(Post.published_at.desc()).offset(offset).limit(limit).all()
    return [_post_to_response(p) for p in posts]


@router.get("/slug/{slug}", response_model=PostResponse)
def get_post_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    post = db.query(Post).options(joinedload(Post.author)).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not post.published_at and (not user or post.author_id != user.id):
        raise HTTPException(status_code=404, detail="Post not found")
    return _post_to_response(post)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    post = db.query(Post).options(joinedload(Post.author)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not post.published_at and (not user or post.author_id != user.id):
        raise HTTPException(status_code=404, detail="Post not found")
    return _post_to_response(post)


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: UUID,
    data: PostUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.query(Post).options(joinedload(Post.author)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this post")
    if data.title is not None:
        post.title = data.title
    if data.body is not None:
        post.body = data.body
    if data.body_format is not None:
        post.body_format = data.body_format
    if data.cover_image_url is not None:
        post.cover_image_url = data.cover_image_url
    if data.published is not None:
        post.published_at = datetime.utcnow() if data.published else None
    db.commit()
    db.refresh(post)
    return _post_to_response(post)


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this post")
    db.delete(post)
    db.commit()
    return None

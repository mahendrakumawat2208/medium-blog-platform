from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user, get_current_user_optional
from app.core.database import get_db
from app.models.user import User
from app.models.post import Post
from app.models.follow import Follow
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.post import PostResponse, PostAuthor

router = APIRouter(prefix="/users", tags=["users"])


def _user_to_response(user: User) -> UserResponse:
    return UserResponse.model_validate(user)


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


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return _user_to_response(user)


@router.patch("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if data.display_name is not None:
        user.display_name = data.display_name
    if data.bio is not None:
        user.bio = data.bio
    if data.avatar_url is not None:
        user.avatar_url = data.avatar_url
    db.commit()
    db.refresh(user)
    return _user_to_response(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_response(user)


@router.get("/by-username/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_response(user)


@router.get("/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(
    user_id: UUID,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    q = db.query(Post).options(joinedload(Post.author)).filter(Post.author_id == user_id, Post.published_at.isnot(None))
    posts = q.order_by(Post.published_at.desc()).offset(offset).limit(limit).all()
    return [_post_to_response(p) for p in posts]


@router.post("/me/follow/{user_id}", status_code=204)
def follow_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if db.query(Follow).filter(Follow.follower_id == current_user.id, Follow.following_id == user_id).first():
        return None
    follow = Follow(follower_id=current_user.id, following_id=user_id)
    db.add(follow)
    db.commit()
    return None


@router.delete("/me/follow/{user_id}", status_code=204)
def unfollow_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow = db.query(Follow).filter(Follow.follower_id == current_user.id, Follow.following_id == user_id).first()
    if follow:
        db.delete(follow)
        db.commit()
    return None

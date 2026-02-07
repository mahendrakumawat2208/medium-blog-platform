from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user_optional
from app.core.database import get_db
from app.models.user import User
from app.models.post import Post
from app.models.follow import Follow
from app.schemas.post import PostResponse, PostAuthor

router = APIRouter(prefix="/feed", tags=["feed"])


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


@router.get("", response_model=list[PostResponse])
def get_feed(
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    if user:
        following_ids = [r[0] for r in db.query(Follow.following_id).filter(Follow.follower_id == user.id).all()]
        if following_ids:
            q = (
                db.query(Post)
                .options(joinedload(Post.author))
                .filter(Post.published_at.isnot(None), Post.author_id.in_(following_ids))
            )
        else:
            q = db.query(Post).options(joinedload(Post.author)).filter(Post.published_at.isnot(None))
    else:
        q = db.query(Post).options(joinedload(Post.author)).filter(Post.published_at.isnot(None))
    posts = q.order_by(Post.published_at.desc()).offset(offset).limit(limit).all()
    return [_post_to_response(p) for p in posts]

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Follow(Base):
    __tablename__ = "follows"
    __table_args__ = (UniqueConstraint("follower_id", "following_id", name="uq_follow"),)

    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    follower = relationship("User", back_populates="following", foreign_keys=[follower_id])
    following = relationship("User", back_populates="followers", foreign_keys=[following_id])

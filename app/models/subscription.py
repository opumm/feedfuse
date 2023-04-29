from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .feeds import Feed  # noqa: F401
    from .users import User  # noqa: F401


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    feed_id = Column(Integer, ForeignKey("feed.id"))

    subscription_user = relationship("User", back_populates="user_subscription")
    subscription_feed = relationship("Feed", back_populates="feed_subscription")

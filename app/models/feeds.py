from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .items import Item  # noqa: F401
    from .subscription import Subscription  # noqa: F401


class Feed(Base):
    __tablename__ = "feed"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    url = Column(String, nullable=False, index=True)
    description = Column(String)
    last_built_at = Column(DateTime, default=None)
    is_update_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    feed_item = relationship("Item", back_populates="item_feed")
    feed_subscription = relationship("Subscription", back_populates="subscription_feed")

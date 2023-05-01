from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .feeds import Feed  # noqa: F401
    from .read_status import ReadStatus  # noqa: F401


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, index=True)
    guid = Column(String, nullable=False, index=True)
    description = Column(String, default=None)
    published_at = Column(DateTime)
    feed_id = Column(
        Integer, ForeignKey("feed.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    read_status = relationship(
        "ReadStatus", backref="item", cascade="all, delete-orphan"
    )

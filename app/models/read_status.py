from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .items import Item  # noqa: F401
    from .users import User  # noqa: F401


class ReadStatus(Base):
    __tablename__ = "read_status"

    id = Column(Integer, primary_key=True, index=True)
    is_read = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    item_id = Column(Integer, ForeignKey("item.id"))

    read_status_user = relationship("User", back_populates="user_read_status")
    read_status_item = relationship("Item", back_populates="item_read_status")

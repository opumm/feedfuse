from typing import TYPE_CHECKING

from passlib.context import CryptContext
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .read_status import ReadStatus  # noqa: F401
    from .subscription import Subscription  # noqa: F401

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    user_subscription = relationship("Subscription", back_populates="subscription_user")
    user_read_status = relationship("ReadStatus", back_populates="read_status_user")

    @property
    def password(self) -> None:
        raise ValueError("Password is write-only")

    @password.setter
    def password(self, value) -> None:
        self.hashed_password = pwd_context.hash(value)

    def verify_password(self, password) -> bool:
        return pwd_context.verify(password, self.hashed_password)

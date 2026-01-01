from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from database import Base

class UserRole(str, enum.Enum):
    """User role enumeration"""
    BUYER = "buyer"
    SELLER = "seller"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.BUYER)
    is_active = Column(Integer, default=1)  # MySQL doesn't have native boolean
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship with products
    products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    ANALYST = "Analyst"
    VIEWER = "Viewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.VIEWER)

    # Relationship: A user can have multiple transactions
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete-orphan")
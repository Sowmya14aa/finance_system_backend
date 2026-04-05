from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum
from datetime import datetime

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String(100), nullable=False) # e.g., Food, Salary, Rent
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String(255), nullable=True)
    
    # Foreign Key: Links the transaction to a specific user
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship: Links back to the User model
    owner = relationship("User", back_populates="transactions")
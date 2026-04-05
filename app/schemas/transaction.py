from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    type: TransactionType
    category: str
    notes: Optional[str] = None
    date: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True

# For the Analytics Requirement
class FinanceSummary(BaseModel):
    total_income: float
    total_expenses: float
    current_balance: float
    recent_transactions: List[TransactionResponse]
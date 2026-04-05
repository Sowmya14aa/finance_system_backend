from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.transaction_service import TransactionService
from app.api.deps import get_current_user # Import the security guard
from app.models.user import User

router = APIRouter()

@router.get("/summary")
def get_finance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Get the real user from the token
):
    return TransactionService.get_finance_summary(db, user_id=current_user.id)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import csv
import io

from app.db.session import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.models.transaction import TransactionType
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# --- CSV EXPORT ROUTE ---
@router.get("/export/csv")
def export_transactions_csv(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Export all transactions for the logged-in user to a CSV file.
    """
    # Fetch records (Using the service with no limit for export)
    transactions = TransactionService.get_transactions(db, user_id=current_user.id, limit=None)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Date", "Category", "Type", "Amount", "Description"])
    
    for t in transactions:
        writer.writerow([t.id, t.date, t.category, t.type.value, t.amount, t.description])
    
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=transactions_{current_user.username}.csv"}
    )

# --- GET ALL WITH PAGINATION & SEARCH ---
@router.get("/", response_model=List[TransactionResponse])
def read_transactions(
    type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, le=100, description="Maximum records to return"),
    search: Optional[str] = Query(None, description="Search term for descriptions"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves a paginated list of transactions with optional filters.
    """
    return TransactionService.get_transactions(
        db, 
        user_id=current_user.id, 
        type=type, 
        category=category, 
        start_date=start_date, 
        end_date=end_date,
        skip=skip,
        limit=limit,
        search=search
    )

# --- CREATE TRANSACTION ---
@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_in: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Only Admins or Analysts should typically create records in high-security systems, 
    but for this assignment, we allow the user to create their own records.
    """
    return TransactionService.create_transaction(db, transaction_in, user_id=current_user.id)

# --- GET SINGLE TRANSACTION ---
@router.get("/{transaction_id}", response_model=TransactionResponse)
def read_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = TransactionService.get_transaction_by_id(db, transaction_id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found or unauthorized")
    return transaction

# --- DELETE TRANSACTION (RBAC ENFORCED) ---
@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # CRITICAL ROLE CHECK
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only Admins have permission to delete transactions"
        )
        
    success = TransactionService.delete_transaction(db, transaction_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return None
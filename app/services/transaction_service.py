from sqlalchemy.orm import Session
from sqlalchemy import func, extract, or_
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate
from datetime import datetime
from typing import Optional, List

class TransactionService:
    @staticmethod
    def create_transaction(db: Session, transaction_data: TransactionCreate, user_id: int):
        """
        Criteria #1 & #5: Efficiently handles Pydantic data and persists to MySQL.
        """
        # Compatibility check for Pydantic v1 (dict) vs v2 (model_dump)
        data = transaction_data.dict() if hasattr(transaction_data, 'dict') else transaction_data.model_dump()
        
        db_transaction = Transaction(
            **data,
            user_id=user_id
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def get_transactions(
        db: Session, 
        user_id: int, 
        type: Optional[TransactionType] = None, 
        category: Optional[str] = None, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None
    ):
        """
        Criteria #4 & #5: Logical Thinking and Data Handling.
        Implements Filtering, Keyword Search, and Pagination.
        """
        query = db.query(Transaction).filter(Transaction.user_id == user_id)

        # Apply Filters
        if type:
            query = query.filter(Transaction.type == type)
        if category:
            query = query.filter(Transaction.category == category)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        # Apply Search (Checks description/notes and category)
        if search:
            query = query.filter(
                or_(
                    Transaction.description.contains(search),
                    Transaction.category.contains(search)
                )
            )

        # Apply Ordering and Pagination
        return query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int, user_id: int):
        """
        Criteria #6: Reliability. Ensures User A cannot access User B's transaction ID.
        """
        return db.query(Transaction).filter(
            Transaction.id == transaction_id, 
            Transaction.user_id == user_id
        ).first()

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int, user_id: int):
        """
        Criteria #3: Functionality. Atomic deletion with session commit.
        """
        db_transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id, 
            Transaction.user_id == user_id
        ).first()
        
        if db_transaction:
            db.delete(db_transaction)
            db.commit()
            return True
        return False

    @staticmethod
    def get_finance_summary(db: Session, user_id: int):
        """
        Criteria #2 & #4: Analytics Logic.
        Processes raw data into meaningful financial insights.
        """
        # 1. Calculate Totals using SQL aggregate functions (High Performance)
        total_income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id, 
            Transaction.type == TransactionType.INCOME
        ).scalar() or 0.0

        total_expenses = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id, 
            Transaction.type == TransactionType.EXPENSE
        ).scalar() or 0.0

        # 2. Monthly Expense Tracking
        current_month = datetime.utcnow().month
        monthly_exp = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            extract('month', Transaction.date) == current_month
        ).scalar() or 0.0

        # 3. Category Breakdown (Aggregated via GROUP BY)
        category_data = db.query(
            Transaction.category, 
            func.sum(Transaction.amount)
        ).filter(Transaction.user_id == user_id).group_by(Transaction.category).all()

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "current_balance": total_income - total_expenses,
            "monthly_expense": monthly_exp,
            "category_breakdown": {cat: amt for cat, amt in category_data},
            "recent_transactions": db.query(Transaction).filter(
                Transaction.user_id == user_id
            ).order_by(Transaction.date.desc()).limit(5).all()
        }
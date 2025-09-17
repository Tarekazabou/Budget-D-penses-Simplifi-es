from sqlmodel import Session, select, and_, func
from app.models.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionType
from datetime import date, datetime, timedelta
from typing import List, Optional

def create_transaction(db: Session, transaction: TransactionCreate, user_id: str) -> Transaction:
    """Créer une nouvelle transaction"""
    db_transaction = Transaction(
        **transaction.dict(),
        user_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction_by_id(db: Session, transaction_id: str, user_id: str) -> Optional[Transaction]:
    """Récupérer une transaction par ID"""
    statement = select(Transaction).where(
        and_(Transaction.transaction_id == transaction_id, Transaction.user_id == user_id)
    )
    return db.exec(statement).first()

def get_transactions(
    db: Session, 
    user_id: str, 
    skip: int = 0, 
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    transaction_type: Optional[TransactionType] = None,
    category: Optional[str] = None
) -> List[Transaction]:
    """Récupérer les transactions avec filtres"""
    statement = select(Transaction).where(Transaction.user_id == user_id)
    
    if start_date:
        statement = statement.where(Transaction.date >= start_date)
    if end_date:
        statement = statement.where(Transaction.date <= end_date)
    if transaction_type:
        statement = statement.where(Transaction.type == transaction_type)
    if category:
        statement = statement.where(Transaction.category == category)
    
    statement = statement.offset(skip).limit(limit).order_by(Transaction.date.desc())
    return db.exec(statement).all()

def update_transaction(
    db: Session, 
    transaction_id: str, 
    user_id: str, 
    transaction_update: TransactionUpdate
) -> Optional[Transaction]:
    """Mettre à jour une transaction"""
    db_transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not db_transaction:
        return None
    
    update_data = transaction_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: str, user_id: str) -> bool:
    """Supprimer une transaction"""
    db_transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not db_transaction:
        return False
    
    db.delete(db_transaction)
    db.commit()
    return True

def get_balance(db: Session, user_id: str, start_date: date, end_date: date) -> dict:
    """Calculer le solde (revenus - dépenses) pour une période"""
    # Revenus
    income_statement = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.INCOME,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    )
    total_income = db.exec(income_statement).first() or 0
    
    # Dépenses
    expense_statement = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    )
    total_expenses = db.exec(expense_statement).first() or 0
    
    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "balance": float(total_income) - float(total_expenses)
    }

def get_expenses_by_category(
    db: Session, 
    user_id: str, 
    start_date: date, 
    end_date: date
) -> List[dict]:
    """Obtenir les dépenses regroupées par catégorie"""
    statement = select(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).where(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).group_by(Transaction.category)
    
    results = db.exec(statement).all()
    return [{"category": category, "amount": float(total)} for category, total in results]
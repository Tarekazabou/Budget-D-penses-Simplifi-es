from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import date, datetime, timedelta

from app.core.database import get_session
from app.dependencies import get_current_user
from app.crud.transaction import (
    create_transaction, 
    get_transactions, 
    get_transaction_by_id,
    update_transaction,
    delete_transaction
)
from app.models.user import User
from app.models.transaction import (
    TransactionCreate, 
    TransactionUpdate, 
    TransactionResponse,
    TransactionType
)

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
async def create_new_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Créer une nouvelle transaction"""
    db_transaction = create_transaction(db=db, transaction=transaction, user_id=current_user.user_id)
    return TransactionResponse(
        transaction_id=db_transaction.transaction_id,
        user_id=db_transaction.user_id,
        amount=db_transaction.amount,
        type=db_transaction.type,
        category=db_transaction.category,
        description=db_transaction.description,
        date=db_transaction.date,
        created_at=db_transaction.created_at
    )

@router.get("/", response_model=List[TransactionResponse])
async def read_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    transaction_type: Optional[TransactionType] = Query(None),
    category: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Récupérer les transactions de l'utilisateur"""
    transactions = get_transactions(
        db=db,
        user_id=current_user.user_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type,
        category=category
    )
    
    return [
        TransactionResponse(
            transaction_id=t.transaction_id,
            user_id=t.user_id,
            amount=t.amount,
            type=t.type,
            category=t.category,
            description=t.description,
            date=t.date,
            created_at=t.created_at
        ) for t in transactions
    ]

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def read_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Récupérer une transaction spécifique"""
    transaction = get_transaction_by_id(db=db, transaction_id=transaction_id, user_id=current_user.user_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        user_id=transaction.user_id,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        description=transaction.description,
        date=transaction.date,
        created_at=transaction.created_at
    )

@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction_endpoint(
    transaction_id: str,
    transaction_update: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Mettre à jour une transaction"""
    updated_transaction = update_transaction(
        db=db,
        transaction_id=transaction_id,
        user_id=current_user.user_id,
        transaction_update=transaction_update
    )
    
    if not updated_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return TransactionResponse(
        transaction_id=updated_transaction.transaction_id,
        user_id=updated_transaction.user_id,
        amount=updated_transaction.amount,
        type=updated_transaction.type,
        category=updated_transaction.category,
        description=updated_transaction.description,
        date=updated_transaction.date,
        created_at=updated_transaction.created_at
    )

@router.delete("/{transaction_id}")
async def delete_transaction_endpoint(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Supprimer une transaction"""
    success = delete_transaction(db=db, transaction_id=transaction_id, user_id=current_user.user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return {"message": "Transaction deleted successfully"}
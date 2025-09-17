from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional
from datetime import date, datetime, timedelta

from app.core.database import get_session
from app.dependencies import get_current_user
from app.crud.transaction import get_balance, get_expenses_by_category
from app.models.user import User

router = APIRouter()

@router.get("/balance")
async def get_dashboard_balance(
    period: str = Query("monthly", regex="^(weekly|monthly|yearly)$"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Obtenir le solde pour le tableau de bord"""
    
    # Si les dates ne sont pas fournies, calculer selon la période
    if not start_date or not end_date:
        today = date.today()
        
        if period == "weekly":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif period == "monthly":
            start_date = today.replace(day=1)
            # Dernier jour du mois
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        elif period == "yearly":
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
    
    balance = get_balance(db=db, user_id=current_user.user_id, start_date=start_date, end_date=end_date)
    
    return {
        **balance,
        "period": period,
        "start_date": start_date,
        "end_date": end_date
    }

@router.get("/expenses-by-category")
async def get_dashboard_expenses_by_category(
    period: str = Query("monthly", regex="^(weekly|monthly|yearly)$"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Obtenir la répartition des dépenses par catégorie"""
    
    # Si les dates ne sont pas fournies, calculer selon la période
    if not start_date or not end_date:
        today = date.today()
        
        if period == "weekly":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif period == "monthly":
            start_date = today.replace(day=1)
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        elif period == "yearly":
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
    
    expenses = get_expenses_by_category(
        db=db, 
        user_id=current_user.user_id, 
        start_date=start_date, 
        end_date=end_date
    )
    
    return {
        "expenses_by_category": expenses,
        "period": period,
        "start_date": start_date,
        "end_date": end_date
    }

@router.get("/summary")
async def get_dashboard_summary(
    period: str = Query("monthly", regex="^(weekly|monthly|yearly)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Obtenir un résumé complet pour le tableau de bord"""
    
    # Calculer les dates selon la période
    today = date.today()
    
    if period == "weekly":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == "monthly":
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    elif period == "yearly":
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    
    # Obtenir le solde
    balance = get_balance(db=db, user_id=current_user.user_id, start_date=start_date, end_date=end_date)
    
    # Obtenir les dépenses par catégorie
    expenses = get_expenses_by_category(
        db=db, 
        user_id=current_user.user_id, 
        start_date=start_date, 
        end_date=end_date
    )
    
    return {
        "balance": balance,
        "expenses_by_category": expenses,
        "period": period,
        "start_date": start_date,
        "end_date": end_date
    }
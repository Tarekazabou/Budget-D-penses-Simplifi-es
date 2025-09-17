from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class BudgetPeriod(str, Enum):
    """Périodes de budget"""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class BudgetBase(SQLModel):
    """Modèle de base pour les budgets"""
    category: str = Field(description="Catégorie du budget (ex: courses, transport, global)")
    limit_amount: float = Field(gt=0, description="Montant limite du budget")
    period: BudgetPeriod = Field(default=BudgetPeriod.MONTHLY)

class Budget(BudgetBase, table=True):
    """Modèle budget pour la base de données"""
    budget_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.user_id")
    current_spent: float = Field(default=0.0, description="Montant déjà dépensé")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class BudgetCreate(BudgetBase):
    """Modèle pour la création d'un budget"""
    pass

class BudgetUpdate(SQLModel):
    """Modèle pour la mise à jour d'un budget"""
    limit_amount: Optional[float] = None
    period: Optional[BudgetPeriod] = None

class BudgetResponse(BudgetBase):
    """Modèle de réponse budget"""
    budget_id: str
    user_id: str
    current_spent: float
    remaining: float = Field(description="Montant restant")
    is_exceeded: bool = Field(description="Budget dépassé ou non")
    created_at: datetime
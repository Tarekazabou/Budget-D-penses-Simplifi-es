from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum
import uuid

class TransactionType(str, Enum):
    """Types de transaction"""
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCategory(str, Enum):
    """Catégories de transaction"""
    # Revenus
    SALARY = "salaire"
    FREELANCE = "freelance"
    INVESTMENT = "investissement"
    OTHER_INCOME = "autre_revenu"
    
    # Dépenses
    GROCERIES = "courses"
    RENT = "loyer"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    ENTERTAINMENT = "divertissement"
    HEALTHCARE = "sante"
    EDUCATION = "education"
    CLOTHING = "vetements"
    RESTAURANT = "restaurant"
    OTHER_EXPENSE = "autre_depense"

class TransactionBase(SQLModel):
    """Modèle de base pour les transactions"""
    amount: float = Field(gt=0, description="Montant de la transaction")
    type: TransactionType
    category: TransactionCategory
    description: Optional[str] = None
    date: date = Field(default_factory=date.today)

class Transaction(TransactionBase, table=True):
    """Modèle transaction pour la base de données"""
    transaction_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.user_id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class TransactionCreate(TransactionBase):
    """Modèle pour la création d'une transaction"""
    pass

class TransactionUpdate(SQLModel):
    """Modèle pour la mise à jour d'une transaction"""
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    description: Optional[str] = None
    date: Optional[date] = None

class TransactionResponse(TransactionBase):
    """Modèle de réponse transaction"""
    transaction_id: str
    user_id: str
    created_at: datetime
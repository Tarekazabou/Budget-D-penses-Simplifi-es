from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class AlertType(str, Enum):
    """Types d'alerte"""
    BUDGET_EXCEEDED = "budget_exceeded"
    BUDGET_WARNING = "budget_warning"  # 80% du budget atteint
    UNUSUAL_SPENDING = "unusual_spending"

class AlertBase(SQLModel):
    """Modèle de base pour les alertes"""
    message: str = Field(description="Message de l'alerte")
    alert_type: AlertType
    category: str = Field(description="Catégorie concernée")
    is_read: bool = Field(default=False)

class Alert(AlertBase, table=True):
    """Modèle alerte pour la base de données"""
    alert_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.user_id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class AlertCreate(AlertBase):
    """Modèle pour la création d'une alerte"""
    pass

class AlertResponse(AlertBase):
    """Modèle de réponse alerte"""
    alert_id: str
    user_id: str
    created_at: datetime
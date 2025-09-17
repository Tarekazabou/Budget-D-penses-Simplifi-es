from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    """Modèle de base pour l'utilisateur"""
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    """Modèle utilisateur pour la base de données"""
    user_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    """Modèle pour la création d'un utilisateur"""
    password: str

class UserResponse(UserBase):
    """Modèle de réponse utilisateur (sans mot de passe)"""
    user_id: str
    created_at: datetime
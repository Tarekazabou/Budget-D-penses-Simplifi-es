from sqlmodel import Session, select
from app.models.user import User, UserCreate
from app.core.security import get_password_hash, verify_password
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Récupérer un utilisateur par email"""
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Récupérer un utilisateur par ID"""
    statement = select(User).where(User.user_id == user_id)
    return db.exec(statement).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Créer un nouvel utilisateur"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authentifier un utilisateur"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Création du moteur de base de données
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

def create_db_and_tables():
    """Créer la base de données et les tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Obtenir une session de base de données"""
    with Session(engine) as session:
        yield session
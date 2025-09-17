from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.routers import auth, transactions, budgets, dashboard

# Chargement des variables d'environnement
load_dotenv()

# Création de l'application FastAPI
app = FastAPI(
    title="Budget & Dépenses Simplifiées API",
    description="API pour la gestion des finances personnelles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(budgets.router, prefix="/api/v1/budgets", tags=["budgets"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "Budget & Dépenses Simplifiées API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
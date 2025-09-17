from fastapi import APIRouter

# Placeholder pour les endpoints budgets (à implémenter)
router = APIRouter()

@router.get("/")
async def get_budgets():
    """Récupérer les budgets de l'utilisateur"""
    return {"message": "Budgets endpoint - à implémenter"}

@router.post("/")
async def create_budget():
    """Créer un nouveau budget"""
    return {"message": "Create budget endpoint - à implémenter"}
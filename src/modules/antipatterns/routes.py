from fastapi import APIRouter
from antipatterns.controllers import evaluate_antipattern
from models import AntipatternRequest

# Crear un router
antipatterns_router = APIRouter()


# Define las rutas
@antipatterns_router.post("/evaluate")
def evaluate(request: AntipatternRequest):
    return evaluate_antipattern(request.code, request.antipatterns)

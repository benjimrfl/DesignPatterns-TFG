from fastapi import APIRouter
from src.modules.inappropiate_patterns.models import InappropiatePatternRequest
from src.modules.inappropiate_patterns.controllers import InappropiatePatternController

# Crear un router
inappropiate_patterns_router = APIRouter()

# Define las rutas
@inappropiate_patterns_router.post("/evaluate")
async def evaluate(request: InappropiatePatternRequest):
    print("LLAMANDO AL CONTROLADOR")
    return await InappropiatePatternController.evaluate_inappropiate_pattern(request.code, request.inappropiatePatterns)

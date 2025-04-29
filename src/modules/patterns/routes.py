from fastapi import APIRouter
from src.modules.patterns.models import PatternRequest
from src.modules.patterns.controllers import PatternController

# Crear un router
patterns_router = APIRouter()

# Define las rutas
@patterns_router.post("/evaluate")
async def evaluate(request: PatternRequest):
    print("LLAMANDO AL CONTROLADOR")
    return await PatternController.evaluate_pattern(request.code, request.pattern, request.patternList)

@patterns_router.post("/evaluateYN")
async def evaluateYN(template: dict):
    print("LLAMANDO AL CONTROLADOR")
    return await PatternController.evaluate_YN(template)

from fastapi import APIRouter
from src.modules.patterns.models import PatternRequest, EvalItem
from src.modules.patterns.controllers import PatternController

# Crear un router
patterns_router = APIRouter()

# Define las rutas
@patterns_router.post("/evaluate")
async def evaluate(request: PatternRequest):
    print("LLAMANDO AL CONTROLADOR")
    return await PatternController.evaluate_pattern(request.code, request.pattern, request.patternList)

@patterns_router.post("/evaluateYN")
async def evaluateYN(payload: list[EvalItem]):
    print("LLAMANDO AL CONTROLADOR")
    return await PatternController.evaluate_YN(payload)

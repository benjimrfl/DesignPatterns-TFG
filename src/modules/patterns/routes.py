from fastapi import APIRouter, Path
from src.modules.patterns.models import PatternRequest
from src.modules.patterns.controllers import PatternController

# Crear un router
patterns_router = APIRouter()

# Define las rutas
@patterns_router.post("/evaluate")
async def evaluate(request: PatternRequest):
    print("LLAMANDO AL CONTROLADOR")
    return await PatternController.evaluate_pattern(request.code, request.pattern, request.patternList)

@patterns_router.post("/evaluateYN/{model}")
async def evaluateYN(template: dict, model: str = Path(..., description="Nombre del modelo, e.g. 'gemini', 'openai'")):
    print("LLAMANDO AL CONTROLADOR")
    return await PatternController.evaluate_YN(template, model)

@patterns_router.post("/evaluateJSON/{model}")
async def evaluateJSON(template: dict, model: str = Path(..., description="Nombre del modelo, e.g. 'gemini', 'openai'")):
    print("LLAMANDO AL CONTROLADOR")
    return await PatternController.evaluate_json(template, model)

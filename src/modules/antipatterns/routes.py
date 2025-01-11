from fastapi import APIRouter
from src.modules.antipatterns.models import AntipatternRequest
from src.modules.antipatterns.controllers import AntipatternController

# Crear un router
antipatterns_router = APIRouter()

# Define las rutas
@antipatterns_router.post("/evaluate")
async def evaluate(request: AntipatternRequest):
    print("LLAMANDO AL CONTROLADOR")
    return await AntipatternController.evaluate_antipattern(request.code, request.antipatterns)

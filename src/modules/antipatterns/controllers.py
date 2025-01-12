from fastapi import HTTPException
from src.modules.antipatterns.services import AntipatternService

class AntipatternController:
    async def evaluate_antipattern(code, antipatterns):
        try:
            # Llamar al servicio de negocio
            print("LLAMANDO AL SERVICIO")
            result = await AntipatternService().evaluate(code, antipatterns)

            # Devolver respuesta
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

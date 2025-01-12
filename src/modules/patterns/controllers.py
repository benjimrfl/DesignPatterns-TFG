from fastapi import HTTPException
from src.modules.patterns.services import PatternService

class PatternController:
    async def evaluate_pattern(code, pattern):
        try:
            print("LLAMANDO AL SERVICIO")
            # Llamar al servicio de negocio
            result = await PatternService().evaluate(code, pattern)

            # Devolver respuesta
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

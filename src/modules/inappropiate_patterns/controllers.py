from fastapi import HTTPException
from src.modules.inappropiate_patterns.services import InappropiatePatternervice

class InappropiatePatternController:
    async def evaluate_inappropiate_pattern(code, inappropiatePatterns):
        try:
            # Llamar al servicio de negocio
            print("LLAMANDO AL SERVICIO")
            result = await InappropiatePatternervice().evaluate(code, inappropiatePatterns)

            # Devolver respuesta
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

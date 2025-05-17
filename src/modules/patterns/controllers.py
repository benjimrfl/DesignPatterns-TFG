from fastapi import HTTPException
from src.modules.patterns.services import PatternService

class PatternController:
    async def evaluate_pattern(code, pattern, patternList=None, model="gemini"):
        try:
            print("LLAMANDO AL SERVICIO")
            # Llamar al servicio de negocio
            result = await PatternService().evaluate(code, pattern, model, patternList)

            # Devolver respuesta
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def evaluate_YN(template, model):
        try:
            print("LLAMANDO AL SERVICIO")
            # Llamar al servicio de negocio
            result = await PatternService().evaluate_YN(template, model)

            # Devolver respuesta
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def evaluate_json(template, model):
        try:
            print("LLAMANDO AL SERVICIO")
            # Llamar al servicio de negocio
            result = await PatternService().evaluate_json(template, model)

            # Devolver respuesta
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
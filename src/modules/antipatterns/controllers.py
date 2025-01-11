from fastapi import HTTPException
from src.modules.antipatterns.services import AntipatternService

class AntipatternController:
    async def evaluate_antipattern(code, antipatterns):
        try:
            # Validar la longitud del código
            if len(code) > 250:
                raise HTTPException(
                    status_code=400, 
                    detail="The code exceeds the maximum allowed length of 250 characters."
                )

            # Llamar al servicio de negocio
            print("LLAMANDO AL SERVICIO")
            print(antipatterns)
            print("CODIGO: ")
            print(code)
            result = await AntipatternService().evaluate(code, antipatterns)

            # Devolver respuesta
            return result, 200

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

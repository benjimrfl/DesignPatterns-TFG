from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()

            # Restaurar el cuerpo para las siguientes etapas
            async def receive_body():
                return {"type": "http.request", "body": body, "more_body": False}

            request = Request(scope=request.scope, receive=receive_body)

        try:
            # Procesar la solicitud y capturar excepciones
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error al procesar la solicitud: {e}")
            raise

        # Registrar la respuesta
        logger.info(f"Response Status Code: {response.status_code}")

        return response

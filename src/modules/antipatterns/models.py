from pydantic import BaseModel  # Importa BaseModel desde pydantic

class AntipatternRequest(BaseModel):
    code: str  # Por ejemplo, el código fuente a evaluar
    antipatterns: list  # Lenguaje del código (Python, Java, etc.)
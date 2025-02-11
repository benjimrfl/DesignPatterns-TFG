from typing import Optional
from pydantic import BaseModel, field_validator  # Importa BaseModel desde pydantic

class PatternRequest(BaseModel):
    code: str  # Código fuente a evaluar
    pattern: str  # Patron esperado (Python, Java, etc.)
    patternList: Optional[list] = None  # Lista opcional
    
    @field_validator("code")
    def validate_code_length(cls, value):
        if len(value) > 250:
            raise ValueError("The code must be less than 250 characters.")
        return value
    
    @field_validator("patternList", mode="before")
    def validate_pattern_list(cls, value):
        if value is not None:
            if len(value) != 3:
                raise ValueError("patternList must have exactly 3 elements.")
        return value
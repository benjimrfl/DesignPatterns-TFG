from pydantic import BaseModel, field_validator 

class AntipatternRequest(BaseModel):
    code: str
    antipatterns: list

    # Validador para el campo `code`
    @field_validator("code")
    def validate_code_length(cls, value):
        if len(value) > 5000:
            raise ValueError("The code must be less than 5000 characters.")
        return value
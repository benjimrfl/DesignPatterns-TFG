from pydantic import BaseModel, field_validator 

class AntipatternRequest(BaseModel):
    code: str
    antipatterns: list

    # Validador para el campo `code`
    @field_validator("code")
    def validate_code_length(cls, value):
        if len(value) > 250:
            raise ValueError("The code must be less than 250 characters.")
        return value
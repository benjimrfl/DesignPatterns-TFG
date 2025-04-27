from pydantic import BaseModel, field_validator 

class InappropiatePatternRequest(BaseModel):
    code: str
    inappropiatePatterns: list

    # Validador para el campo `code`
    @field_validator("code")
    def validate_code_length(cls, value):
        if len(value) > 5000:
            raise ValueError("The code must be less than 5000 characters.")
        return value
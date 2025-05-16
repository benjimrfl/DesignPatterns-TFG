from google import genai
from fastapi import HTTPException

class GeminiAPI:
    
    def __init__(self, api_key, model="gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def textChat(self, content):
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=content
            )
            return response.text

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate limit" in error_str.lower():
                raise HTTPException(status_code=429, detail="Se alcanzó el límite de uso de Gemini (429 - Too Many Requests).")
            else:
                raise HTTPException(status_code=500, detail=f"Error desconocido al llamar a Gemini: {error_str}")

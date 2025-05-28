from openai import OpenAI
from fastapi import HTTPException

# Configuration constants
BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-reasoner"

class DeepSeekAPI:

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.client = OpenAI(api_key=api_key, base_url=BASE_URL)
        self.model = model

    def textChat(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate limit" in error_str.lower():
                raise HTTPException(status_code=429, detail="Límite de uso de DeepSeek alcanzado (429).")
            else:
                raise HTTPException(status_code=500, detail=f"Error al llamar a DeepSeek: {error_str}")

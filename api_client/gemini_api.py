from google import genai

class GeminiAPI:
    
    def __init__(self, api_key, model = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def textChat(self, content):
        response = self.client.models.generate_content(
            model=self.model,
            contents=content
        )
        return response.text

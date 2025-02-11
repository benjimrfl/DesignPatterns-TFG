from fastapi import HTTPException
import requests

class OllamaAPI:
    BASE_URL = "http://localhost:11434/api/generate"

    def __init__(self, base_url=None):
        if base_url:
            self.BASE_URL = base_url

    async def textChat(self, content):
        try:
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(
                f"{self.BASE_URL}",
                json={"model": "llama3.2",
                    "prompt": content,
                    "stream": False
                    },
                headers=headers
            )
            response.raise_for_status()
            return response.json()    
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
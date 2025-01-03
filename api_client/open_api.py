import requests

class OpenAPI:
    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, base_url=None):
        if base_url:
            self.BASE_URL = base_url

    async def textChat(self, content, authToken):
        headers = {
            "Authorization": f"Bearer {authToken}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            json={"model": "gpt-4o-mini",
                  "messages": [{"role": "developer", "content": content}],
                  "temperature": 0.7
                  },
            headers=headers
        )
        response.raise_for_status()
        return response.json()    
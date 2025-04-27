from fastapi import HTTPException
import requests

class PoetAPI:
    #BASE_URL = "http://150.214.230.39:8081/api/v1"
    BASE_URL = "http://localhost:8000/api/v1"

    def __init__(self, base_url=None):
        if base_url:
            self.BASE_URL = base_url

    # Templates
    def get_all_templates(self):
        """Fetch all templates."""
        response = requests.get(f"{self.BASE_URL}/templates")
        response.raise_for_status()
        return response.json()

    def get_template_by_id(self, template_id):
        """Fetch a template by its ID."""
        response = requests.get(f"{self.BASE_URL}/templates/{template_id}")
        response.raise_for_status()
        return response.json()

    def download_templates_csv(self):
        """Download templates in CSV format."""
        response = requests.get(f"{self.BASE_URL}/templates/download")
        response.raise_for_status()
        return response.content

    # Placeholders
    def get_all_placeholders(self):
        """Fetch all placeholders."""
        response = requests.get(f"{self.BASE_URL}/placeholders")
        response.raise_for_status()
        return response.json()

    def get_placeholders_by_template_id(self, template_id):
        """Fetch placeholders by template ID."""
        response = requests.get(f"{self.BASE_URL}/placeholders/template/{template_id}")
        response.raise_for_status()
        return response.json()

    def get_placeholder_by_id(self, placeholder_id):
        """Fetch a placeholder by its ID."""
        response = requests.get(f"{self.BASE_URL}/placeholders/{placeholder_id}")
        response.raise_for_status()
        return response.json()

    # Input generation
    def generate_inputs(self, n=100):
        """Generate inputs."""
        response = requests.get(f"{self.BASE_URL}/input/generate", params={"n": n})
        response.raise_for_status()
        return response.json()

    def generate_inputs_with_template(self, payload, n=10, mode="random"):
        try:
            params = {"n": n, "mode": mode}
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            """Generate inputs using a template."""
            response = requests.post(
                f"{self.BASE_URL}/input/generateWithTemplate",
                json=payload,
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

    def generate_inputs_with_template_id(self, template_id, n=100, mode="random"):
        """Generate inputs using a template ID."""
        response = requests.get(
            f"{self.BASE_URL}/input/generateWithTemplateId",
            params={"template_id": template_id, "n": n, "mode": mode}
        )
        response.raise_for_status()
        return response.json()

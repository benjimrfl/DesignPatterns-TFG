import json
from api_client.poet_api import PoetAPI
from api_client.eva_api import EvaAPI
from api_client.ollama_api import OllamaAPI
from src.utils import Utils

class AntipatternService:

    async def evaluate(self, code: str, antipatterns: list):
        # Generar entradas usando la API Poet
        payload = self._generate_payload(code, antipatterns)
        response = PoetAPI().generate_inputs_with_template(payload)
        print("GENERANDO RESPUESTAS...")
        data = json.loads(response.content.decode('utf-8'))
        print(data)

        # Evaluar resultados
        return await Utils()._calculate_success_ratio(data, "yes_no")
        

    def _generate_payload(self, code, antipatterns):
        return {
            "base": f"Given the following code: \"{code}\" Is it a good idea to apply the [antipattern] pattern? Answer affirmative or negative",
            "description": "Template to create antippattern application to a designed code",
            "expected_result": "No",
            "placeholders": [
                {
                    "name": "[antipattern]",
                    "description": "Antipattern code",
                    "values": antipatterns,
                }
            ],
        }
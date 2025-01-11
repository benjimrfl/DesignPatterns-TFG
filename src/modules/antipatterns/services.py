import json
from api_client.poet_api import PoetAPI
from api_client.eva_api import EvaAPI
from api_client.ollama_api import OllamaAPI

# Cargar variables de entorno desde .env
# load_dotenv()

# BEARER = os.getenv("BEARER")

class AntipatternService:
    def __init__(self, poet_client=None, eva_client=None, ollama_client=None):
        # Inyección de dependencias
        self.poet_client = poet_client or PoetAPI()
        self.eva_client = eva_client or EvaAPI()
        self.ollama_client = ollama_client or OllamaAPI()

    async def evaluate(self, code: str, antipatterns: list):
        # Generar entradas usando la API Poet
        payload = self._generate_payload(code, antipatterns)
        response = self.poet_client.generate_inputs_with_template(payload)
        print("GENERANDO RESPUESTAS...")
        data = json.loads(response.content.decode('utf-8'))
        print(data)

        # Evaluar resultados
        return await self._calculate_success_ratio(data, "yes_no")
        

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

    async def _evaluate_query(self, query, type, expected_result):
        print("DATA INPUTS:")
        print(query, type, expected_result)
        response = await self.ollama_client.textChat(query)
        print("RESPUESTA OLLAMA: ")
        print(response["response"])
        return self.eva_client.evaluate_output(
            type,
            {"expected_result": expected_result, "generated_result": response["response"]},
        )
    
    async def _calculate_success_ratio(self, data, type_of_evaluation):
        positive_count = 0
        for item in data:
            print("ITEM: ")
            print(item)
            eva_result = await self._evaluate_query(item["query"], type_of_evaluation, item["expected_result"])
            print("EVA RESULT: " + eva_result)
            if eva_result == "pass":
                positive_count += 1

        success_percentage = (positive_count / len(data)) * 100
        return {"evaluation success rate": success_percentage}
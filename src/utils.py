import asyncio
from api_client.eva_api import EvaAPI
from api_client.ollama_api import OllamaAPI
from api_client.gemini_api import GeminiAPI
from api_client.open_api import OpenAPI
import os

# Cargar variables de entorno desde .env
# load_dotenv()

# BEARER = os.getenv("BEARER")

# Clase con métodos accesibles para cualquier módulo
class Utils:
    async def _evaluate_query(self, query, type_of_evaluation, expected_result, model, default="fail"):
        
        match model.lower():
            case "gemini":
                client = GeminiAPI(api_key=os.getenv("GEMINI_API_KEY"))
                response = await client.textChat(query)
            case "ollama":
                response = await OllamaAPI().textChat(query)
                response = response.get("response", "No response key found in API output")
            case "openai":
                response = await OpenAPI().textChat(query, os.getenv("OPENAI_API_KEY"))
            case other:
                raise ValueError(f"Modelo desconocido: {other!r}")

        print(f"RESPUESTA {model.upper()}:")
        print(response)
        eva_result = EvaAPI().evaluate_output(
            type_of_evaluation,
            {"expected_result": expected_result, "generated_result": response, "prompt": query},
            default
        )
        return eva_result, response
    
    async def _calculate_success_ratio(self, data, type_of_evaluation, model, default="fail"):
        positive_count = 0
        negative_cases = []

        for item in data:
            print("ITEM: ")
            print(item)

            # Realiza la evaluación para cada query
            eva_result, generated_result = await self._evaluate_query(item["query"], type_of_evaluation, item["expected_result"], model, default)
            print("EVA RESULT: " + eva_result)

            # Si el resultado es "pass", incrementa el contador
            if eva_result == "pass":
                positive_count += 1
            else:
                # Si el resultado es "fail", agrega el caso a los negativos
                negative_cases.append({
                    "query": item["query"],
                    "expected_result": item["expected_result"],
                    "generated_result": generated_result
                })

        success_percentage = (positive_count / len(data)) * 100

        return {
            "passed cases / total tests": f"{positive_count} / {len(data)}" ,
            "failed cases / total tests": f"{len(negative_cases)} / {len(data)}",
            "evaluation success rate": success_percentage,
            "failed cases": negative_cases  # Devolver también los casos fallidos
        }
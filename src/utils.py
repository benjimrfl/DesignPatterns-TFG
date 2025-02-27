import asyncio
from api_client.eva_api import EvaAPI
from api_client.ollama_api import OllamaAPI

# Cargar variables de entorno desde .env
# load_dotenv()

# BEARER = os.getenv("BEARER")

# Clase con métodos accesibles para cualquier módulo
class Utils:
    async def _evaluate_query(self, query, type_of_evaluation, expected_result, default="fail"):
        response = await OllamaAPI().textChat(query) # Es mejor esperar a que termine de responder a todas las preguntas y pasarlas directamente a EVA??
        generated_result = response["response"]
        print("RESPUESTA OLLAMA: ")
        print(response["response"])
        eva_result = EvaAPI().evaluate_output(
            type_of_evaluation,
            {"expected_result": expected_result, "generated_result": generated_result, "prompt": query},
            default
        )
        return eva_result, generated_result
    
    async def _calculate_success_ratio(self, data, type_of_evaluation, default="fail"):
        positive_count = 0
        negative_cases = []

        for item in data:
            print("ITEM: ")
            print(item)

            # Realiza la evaluación para cada query
            eva_result, generated_result = await self._evaluate_query(item["query"], type_of_evaluation, item["expected_result"], default)
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
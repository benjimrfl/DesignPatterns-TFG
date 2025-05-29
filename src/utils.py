import asyncio
from api_client.eva_api import EvaAPI
from api_client.ollama_api import OllamaAPI
from api_client.gemini_api import GeminiAPI
from api_client.open_api import OpenAPI
from api_client.deepseek_api import DeepSeekAPI
import os
from fastapi import HTTPException

# Cargar variables de entorno desde .env
# load_dotenv()

# BEARER = os.getenv("BEARER")

# Clase con métodos accesibles para cualquier módulo
class Utils:
    async def _call_with_retry(self, func, max_attempts=2, delay=30):
        for attempt in range(max_attempts):
            try:
                result = func()
                if asyncio.iscoroutine(result):
                    result = await result
                return result
            except HTTPException as e:
                if e.status_code == 429 and attempt < max_attempts - 1:
                    print(f"⚠️ Límite alcanzado. Reintentando intento {attempt + 1}/{max_attempts}...")
                    await asyncio.sleep(delay)
                    continue
                raise e

    async def _evaluate_query(self, query, type_of_evaluation, expected_result, model, default="fail"):
        match model.lower():
            case "gemini":
                client = GeminiAPI(api_key=os.getenv("GEMINI_API_KEY"))
                response = await self._call_with_retry(lambda: client.textChat(query))

            case "openai":
                client = OpenAPI(api_key=os.getenv("OPENAI_API_KEY"))
                response = await self._call_with_retry(lambda: client.textChat(query))
                
            case "deepseek":
                client = DeepSeekAPI(api_key=os.getenv("DEEPSEEK_API_KEY"))
                response = await self._call_with_retry(lambda: client.textChat(query))

            case "ollama":
                response = await OllamaAPI().textChat(query)
                response = response.get("response", "No response key found in API output")

            case other:
                raise ValueError(f"Modelo desconocido: {other!r}")

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
            
            if model == "openai" or model == "gemini" or model == "deepseek":
                await asyncio.sleep(1)  # Esperar 1 segundo entre peticiones para evitar problemas de límite de tasa

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
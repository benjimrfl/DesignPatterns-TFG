from api_client.eva_api import EvaAPI
from api_client.ollama_api import OllamaAPI

# Cargar variables de entorno desde .env
# load_dotenv()

# BEARER = os.getenv("BEARER")

class Utils:
    async def _evaluate_query(self, query, type_of_evaluation, expected_result): #metodo comun
        print("DATA INPUTS:")
        print(query, type_of_evaluation, expected_result)
        response = await OllamaAPI().textChat(query)
        print("RESPUESTA OLLAMA: ")
        print(response["response"])
        return EvaAPI().evaluate_output(
            type_of_evaluation,
            {"expected_result": expected_result, "generated_result": response["response"], "prompt": query},
        )
    
    async def _calculate_success_ratio(self, data, type_of_evaluation): #metodo comun
        positive_count = 0
        for item in data:
            print("ITEM: ")
            print(item)
            eva_result = await self._evaluate_query(item["query"], type_of_evaluation, item["expected_result"])
            print("EVA RESULT: " + eva_result)
            if eva_result == "pass":
                positive_count += 1

        success_percentage = (positive_count / len(data)) * 100
        return {"total tests": len(data), "evaluation success rate": success_percentage} 
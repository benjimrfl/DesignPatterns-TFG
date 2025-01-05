import asyncio
import json
from dotenv import load_dotenv
import os
from api_client.poet_api import PoetAPI
from api_client.eva_api import EvaAPI
from api_client.open_api import OpenAPI

# Inicializa los clientes de las APIs
poet_client = PoetAPI()
eva_client = EvaAPI()
chat_client = OpenAPI()

# Cargar variables de entorno desde .env
load_dotenv()

BEARER = os.getenv("BEARER")

async def evaluate_result(query, expected_result):
    response = await chat_client.textChat(query, BEARER)
    print("CHATGPT RESPONSE: ", response.content)
    outputs = {
        "expected_result": expected_result,
        "generated_result": response.content.choices[0].content
        }
    return eva_client.evaluate_output("yes_no", outputs)

def evaluate_code_against_antipatterns(code, antipatterns):
    payload = {
        "base": f"Given the following code: \"{code}\" Is it a good idea to apply the [antipattern] pattern? Answer affirmative or negative",
        "description": "Template to create antippattern application to a designed code",
        "expected_result": "No",
        "placeholders": [
            {
                "name": "[antipattern]",
                "description": "Antipattern code",
                "values": antipatterns
            }
        ]
    }
    response = poet_client.generate_inputs_with_template(payload)

    # Mostrar la respuesta recibida
    print("Respuesta del servidor:")
    print(response.content)
    print("____________________________________________________________________________________")
    # Procesar la respuesta del servidor
    data = json.loads(response.content)

    # Contador para los resultados positivos
    positive_count = 0
    # Evaluar cada consulta
    for item in data:
        eva_result = evaluate_result(item["query"], item["expected_result"])
        print("EVA RESULT: ", eva_result)
        
        # Comparar el resultado de EVA con el resultado esperado
        if eva_result == item["expected_result"]:
            positive_count += 1

    # Calcular el porcentaje de éxito
    total_queries = len(data)
    success_percentage = (positive_count / total_queries) * 100

    return {"evaluation success rate": success_percentage}
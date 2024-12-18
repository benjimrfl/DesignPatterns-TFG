import json
from wsgiref import headers

import requests
from api_client.poet_api import PoetAPI
from api_client.eva_api import EVAAPI

# Inicializa los clientes de las APIs
poet_client = PoetAPI()
eva_client = EVAAPI()

# Ejemplo de código y antipatrones
code_example = """
class DatabaseConnection {
    private static DatabaseConnection instance;

    private DatabaseConnection() {}

    public static DatabaseConnection getInstance() {
        if (instance == null) {
            instance = new DatabaseConnection();
        }
        return instance;
    }
}
"""

antipatterns_example = ["God Object", "Spaghetti Code", "Magic Number", "Singleton"]

def evaluate_antipatterns(code, antipatterns):
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

    try:
        print(json.dumps(payload, indent=4))
        response = poet_client.generate_inputs_with_template(payload)

        # Mostrar la respuesta recibida
        print("Respuesta del servidor:")
        print(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

evaluate_antipatterns(code_example, antipatterns_example)

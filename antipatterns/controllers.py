from flask import request, jsonify
from antipatterns.services import evaluate_code_against_antipatterns

def evaluate_antipattern():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()
        code = data.get("code")
        antipatterns = data.get("antipatterns")

        # Validar los datos
        if not code or not isinstance(code, str) or len(code) > 250:
            return jsonify({"error": "Code must be a string and cannot exceed 250 characters"}), 400

        if not antipatterns or not isinstance(antipatterns, list) or not all(isinstance(ap, str) for ap in antipatterns):
            return jsonify({"error": "Antipatterns must be a list of strings"}), 400

        # Llamar al servicio de negocio
        result = evaluate_code_against_antipatterns(code, antipatterns)

        # Devolver respuesta
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#!/usr/bin/env python3
import logging
import requests
import sys
import os
import csv
import json
import re
from datetime import datetime

# --- Configuración ---
base_url = 'http://localhost:8002'
poet_url = 'http://localhost:8000'
template_ids = ['factory_pattern_code_eval_json']
models = ['deepseek']

csv_filename = "evaluations.csv"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def fetch_template(template_id: str) -> dict:
    url = f"{poet_url}/api/v1/templates/{template_id}"
    logger.info("Solicitando template '%s'...", template_id)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        logger.info("Template '%s' obtenido correctamente.", template_id)
        return data
    except requests.RequestException as e:
        logger.error("Error al solicitar template '%s': %s", template_id, e)
        raise
    except ValueError as e:
        logger.error("Respuesta JSON inválida para template '%s': %s", template_id, e)
        raise


def write_to_csv(row: dict, filename: str):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def evaluate_template(template: dict, model: str) -> dict:
    tid = template.get('id', 'unknown')
    url = f"{base_url}/patterns/evaluateJSON/{model}"
    logger.info("Enviando evaluación para TemplateID = %s con modelo '%s'...", tid, model)
    try:
        resp = requests.post(url, json=template, timeout=120)
        resp.raise_for_status()
        result = resp.json()
    except requests.RequestException as e:
        logger.error("Error en la petición de evaluación (TemplateID = %s, modelo = %s): %s", tid, model, e)
        raise
    except ValueError as e:
        logger.error("Respuesta JSON inválida al evaluar TemplateID = %s con modelo = %s: %s", tid, model, e)
        raise

    passed = result.get('passed cases / total tests', 'N/A')
    failed = result.get('failed cases / total tests', 'N/A')
    rate = result.get('evaluation success rate', 'N/A')
    try:
        rate_display = f"{float(rate):.2f}%"
    except (ValueError, TypeError):
        rate_display = 'N/A'

    # Extraer detalles de los casos fallidos
    failed_cases = result.get("failed cases", [])
    failed_details = []
    for case in failed_cases:
        pattern = tid.split("_")[0]
        failed_details.append({
            "design_pattern": pattern,
            "expected_result": case.get("expected_result", ""),
            "generated_result": case.get("generated_result", "").strip()
        })

    # Escribir al CSV
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "template_id": tid,
        "model": model,
        "passed_cases": passed,
        "failed_cases": failed,
        "success_rate": rate_display,
        "failed_details": json.dumps(failed_details, ensure_ascii=False)
    }

    write_to_csv(row, csv_filename)

    logger.info(
        "Resultado TemplateID = %s, Modelo = '%s' → Passed / Total: %s, Failed / Total: %s, Success Rate: %s",
        tid, model, passed, failed, rate_display
    )

    return result


if __name__ == '__main__':
    total = len(template_ids) * len(models)
    logger.info("Iniciando proceso: %d template(s) x %d modelo(s) = %d solicitudes", len(template_ids), len(models), total)

    for template_id in template_ids:
        try:
            template = fetch_template(template_id)
        except Exception:
            continue

        for model in models:
            try:
                _ = evaluate_template(template, model)
            except Exception:
                continue

    logger.info("Proceso de pruebas finalizado.")

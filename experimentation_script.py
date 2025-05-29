#!/usr/bin/env python3
import logging
import requests
import os
import csv
import json
from datetime import datetime
import time

# --- Configuración ---
base_url = 'http://localhost:8002'
poet_url = 'http://localhost:8000'

template_ids = [
    'adapter_pattern_scenario1_code_eval_json',
    'adapter_pattern_scenario2_code_eval_json',
    'bridge_pattern_scenario1_code_eval_json',
    'bridge_pattern_scenario2_code_eval_json',
    'builder_pattern_scenario1_code_eval_json',
    'builder_pattern_scenario2_code_eval_json',
    'composite_pattern_scenario1_code_eval_json',
    'composite_pattern_scenario2_code_eval_json',
    'decorator_pattern_scenario1_code_eval_json',
    'decorator_pattern_scenario2_code_eval_json',
    'facade_pattern_scenario1_code_eval_json',
    'facade_pattern_scenario2_code_eval_json',
    'factory_pattern_scenario1_code_eval_json',
    'factory_pattern_scenario2_code_eval_json',
    'observer_pattern_scenario1_code_eval_json',
    'observer_pattern_scenario2_code_eval_json',
    'prototype_pattern_scenario1_code_eval_json',
    'prototype_pattern_scenario2_code_eval_json',
    'state_pattern_scenario1_code_eval_json',
    'state_pattern_scenario2_code_eval_json',
    'strategy_pattern_scenario1_code_eval_json',
    'strategy_pattern_scenario2_code_eval_json'
]
models = ['gemini', 'openai', 'deepseek', 'ollama']
runs = [1, 2, 3]

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


def write_to_csv(row: dict, filename: str):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def evaluate_template(template: dict, model: str, template_id: str, run_id: int):
    url = f"{base_url}/patterns/evaluateJSON/{model}"
    logger.info("Enviando evaluación para TemplateID = %s con modelo '%s'...", template_id, model)

    start_time = time.perf_counter()

    try:
        resp = requests.post(url, json=template, timeout=120)
        resp.raise_for_status()
        result = resp.json()
    except requests.RequestException as e:
        logger.error("Error en la petición de evaluación (TemplateID = %s, modelo = %s): %s", template_id, model, e)
        return

    end_time = time.perf_counter()
    duration = round(end_time - start_time, 3)

    try:
        success_rate = float(result.get('evaluation success rate', 0.0))
    except (ValueError, TypeError):
        success_rate = 0.0

    failed_cases = result.get("failed cases", [])
    failed_details = [
        {
            "generated_result": case.get("generated_result", "").strip()
        }
        for case in failed_cases
    ]

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pattern": template_id.split("_")[0].capitalize(),
        "template_id": template_id,
        "model": model,
        "run_id": run_id,
        "success_rate": round(success_rate, 4),
        "duration_seconds": duration,
        "failed_details": json.dumps(failed_details, ensure_ascii=False)
    }

    write_to_csv(row, csv_filename)

    logger.info("Resultado → Success: %.2f%% [%s, %s, run %d, duración %.3fs]",
                success_rate, template_id, model, run_id, duration)

    return result


if __name__ == '__main__':
    total = len(template_ids) * len(models) * len(runs)
    logger.info("Iniciando proceso: %d evaluaciones previstas.", total)

    for template_id in template_ids:
        try:
            template = fetch_template(template_id)
        except Exception:
            continue

        for model in models:
            for run_id in runs:
                try:
                    evaluate_template(template, model, template_id, run_id)
                except Exception as e:
                    logger.error("Error al evaluar %s con modelo %s (escenario %s, run %d): %s",
                                    template_id, model, run_id, e)

    logger.info("Proceso de experimentación finalizado.")

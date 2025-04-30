#!/usr/bin/env python3
"""
Script sencillo para automatizar la evaluación de templates contra múltiples modelos.
Modifica directamente las listas `template_ids` y `models` en el código.
Usa la librería `logging` para generar salidas estructuradas y maneja excepciones de red.
"""
import logging
import requests
import sys

# --- Configuración: modifica aquí los templates y modelos para la experimentación ---
base_url = 'http://localhost:8002'
poet_url = 'http://localhost:8000'
template_ids = ['design_pattern_code_eval_1group_yn']
models = ['openai']

# Configuración básica del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def fetch_template(template_id: str) -> dict:
    """Obtiene un template por ID desde la API de POET."""
    url = f"{poet_url}/api/v1/templates/{template_id}"
    logger.info("Solicitando template '%s'...", template_id)
    try:
        resp = requests.get(url, timeout=10) # los get son rápidos
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


def evaluate_template(template: dict, model: str) -> dict:
    """Evalúa el template contra un modelo específico en el servicio de patterns.
    Extrae y registra métricas clave del resultado."""
    tid = template.get('id', 'unknown')
    url = f"{base_url}/patterns/evaluateYN/{model}"
    logger.info("Enviando evaluación para TemplateID=%s con modelo '%s'...", tid, model)
    try:
        resp = requests.post(url, json=template, timeout=120) # esto puede tardar mucho dependiendo de la template
        resp.raise_for_status()
        result = resp.json()
    except requests.RequestException as e:
        logger.error("Error en la petición de evaluación (TemplateID=%s, modelo=%s): %s", tid, model, e)
        raise
    except ValueError as e:
        logger.error("Respuesta JSON inválida al evaluar TemplateID=%s con modelo=%s: %s", tid, model, e)
        raise

    # Métricas del resultado
    passed = result.get('passed cases / total tests', 'N/A')
    failed = result.get('failed cases / total tests', 'N/A')
    rate = result.get('evaluation success rate', 'N/A')
    try:
        rate_display = f"{float(rate):.2f}%"
    except (ValueError, TypeError):
        rate_display = 'N/A'

    logger.info(
        "Resultado TemplateID=%s, Modelo='%s' → Passed / Total: %s, Failed / Total: %s, Success Rate: %s",
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

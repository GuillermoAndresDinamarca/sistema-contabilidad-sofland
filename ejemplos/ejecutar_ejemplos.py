"""Ejecutor guiado de ejemplos con log y resumen de salidas.

Uso desde la raiz:
    py -3 ejemplos/ejecutar_ejemplos.py
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
LOGS = PROJECT / "logs"
REPORTES = PROJECT / "reportes"
LOGS.mkdir(exist_ok=True)
REPORTES.mkdir(exist_ok=True)

log_path = LOGS / f"ejemplos_{datetime.now():%Y%m%d_%H%M%S}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


ETAPAS = [
    ("01_generar_ejemplos", "generar_ejemplos.py"),
    ("02_generar_casos_especiales", "generar_casos_especiales.py"),
    ("03_generar_casos_practicos", "generar_casos_practicos.py"),
    ("04_analizar_comprobantes", "analizar_casos_contables.py"),
    ("05_validar_anomalias", "validar_datos_contables.py"),
    ("06_pipeline_completo", "pipeline_contable_completo.py"),
]


def ejecutar_etapa(nombre: str, script: str) -> None:
    """Ejecuta una etapa, registra su salida y detiene el flujo ante errores."""
    logger.info("INICIO %s", nombre)
    comando = [sys.executable, str(ROOT / script)]
    if script == "pipeline_contable_completo.py":
        comando.append(str(ROOT))

    entorno = os.environ.copy()
    entorno["PYTHONIOENCODING"] = "utf-8"
    proceso = subprocess.run(
        comando,
        cwd=PROJECT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        env=entorno,
    )
    if proceso.stdout:
        logger.info("%s salida:\n%s", nombre, proceso.stdout.rstrip())
    if proceso.stderr:
        logger.warning("%s advertencias:\n%s", nombre, proceso.stderr.rstrip())
    if proceso.returncode != 0:
        logger.error("FALLO %s con codigo %s", nombre, proceso.returncode)
        raise SystemExit(proceso.returncode)
    logger.info("FIN %s: correcto", nombre)


def resumir_salidas() -> None:
    """Muestra las salidas organizadas del recorrido."""
    logger.info("Salidas Excel en %s", REPORTES)
    for archivo in sorted(REPORTES.glob("*.xlsx")):
        logger.info("  - %s (%s bytes)", archivo.name, archivo.stat().st_size)
    logger.info("Log completo: %s", log_path)


def main() -> None:
    logger.info("=== RECORRIDO GUIADO DE EJEMPLOS ===")
    for nombre, script in ETAPAS:
        ejecutar_etapa(nombre, script)
    resumir_salidas()
    logger.info("=== RECORRIDO FINALIZADO ===")


if __name__ == "__main__":
    main()

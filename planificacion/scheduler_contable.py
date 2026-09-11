"""
scheduler_contable.py
=====================
Planificador de tareas para ejecutar el pipeline contable automáticamente.

Características:
  - Ejecuta pipeline a hora configurada (default: 06:00 AM)
  - Compatible con Windows (Task Scheduler) y Linux/Mac (cron)
  - Registra logs de ejecución
  - Detecta cambios en la carpeta de entrada
  - Ejecuta validación y análisis automáticos

Uso (directo):
    python scheduler_contable.py --time 06:00 --watch

Instalación (Windows Task Scheduler):
    python scheduler_contable.py --install

Instalación (Linux/Mac cron):
    python scheduler_contable.py --install-cron

"""

import os
import sys
import logging
import time
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Importar módulos del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent / "ejemplos"))

try:
    from pipeline_contable_completo import PipelineContable
except ImportError:
    print("Error: Asegúrate de estar en la carpeta del proyecto.")
    sys.exit(1)

from notificador import NotificadorContable

# ──────────────────────────────────────────────────────────────

# Configuración de logging
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / f"scheduler_contable_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s — [%(levelname)s] — %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

# Windows puede iniciar la consola con cp1252; UTF-8 evita fallos al registrar
# los indicadores visuales usados por el pipeline.
for flujo in (sys.stdout, sys.stderr):
    if hasattr(flujo, "reconfigure"):
        flujo.reconfigure(encoding="utf-8", errors="replace")


def validar_hora(valor: str) -> str:
    """Valida y normaliza una hora en formato HH:MM."""
    try:
        hora = datetime.strptime(valor, "%H:%M").strftime("%H:%M")
    except ValueError as exc:
        raise argparse.ArgumentTypeError("La hora debe tener formato HH:MM") from exc
    return hora

# ──────────────────────────────────────────────────────────────

class SchedulerContable:
    """Orquesta la ejecución automática del pipeline contable."""

    def __init__(self, 
                 directorio_entrada: str = "ejemplos",
                 directorio_salida: str = "reportes",
                 hora_ejecucion: str = "06:00"):
        """
        Inicializa el planificador.
        
        Args:
            directorio_entrada: Carpeta con archivos Excel a procesar
            directorio_salida: Carpeta donde guardar reportes
            hora_ejecucion: Hora en formato HH:MM (default: 06:00)
        """
        raiz_proyecto = Path(__file__).resolve().parent.parent
        self.dir_entrada = self._resolver_directorio(directorio_entrada, raiz_proyecto)
        self.dir_salida = self._resolver_directorio(directorio_salida, raiz_proyecto)
        self.hora = hora_ejecucion
        
        # Crear carpetas si no existen
        self.dir_entrada.mkdir(exist_ok=True)
        self.dir_salida.mkdir(exist_ok=True)
        
        logger.info(f"✅ Planificador inicializado")
        logger.info(f"   Entrada: {self.dir_entrada.resolve()}")
        logger.info(f"   Salida: {self.dir_salida.resolve()}")
        logger.info(f"   Hora de ejecución: {self.hora}")

    @staticmethod
    def _resolver_directorio(directorio: str, raiz_proyecto: Path) -> Path:
        """Resuelve rutas relativas respecto de la raíz del proyecto."""
        ruta = Path(directorio).expanduser()
        return ruta if ruta.is_absolute() else raiz_proyecto / ruta

    def ejecutar_pipeline(self):
        """Ejecuta el pipeline y registra resultados."""
        logger.info("=" * 70)
        logger.info("🚀 INICIANDO EJECUCIÓN DEL PIPELINE CONTABLE")
        logger.info("=" * 70)
        
        try:
            # Verificar que hay archivos
            archivos = sorted(
                list(self.dir_entrada.glob("empresa*.xlsx"))
                + [self.dir_entrada / nombre for nombre in (
                    "caso_duplicados.xlsx",
                    "caso_valores_faltantes.xlsx",
                    "caso_tolerancia.xlsx",
                    "caso_conciliacion.xlsx",
                ) if (self.dir_entrada / nombre).exists()]
            )
            if not archivos:
                logger.warning(f"⚠️ No hay archivos Excel en {self.dir_entrada}")
                return False
            
            logger.info(f"📁 Encontrados {len(archivos)} archivos")
            
            # Ejecutar pipeline
            pipeline = PipelineContable(str(self.dir_entrada))
            resultados = pipeline.ejecutar()
            
            # Generar reporte
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta_reporte = self.dir_salida / f"reporte_{timestamp}.xlsx"
            pipeline.generar_reporte_excel(str(ruta_reporte))
            NotificadorContable().notificar_resultados(resultados, ruta_reporte)
            
            logger.info(f"✅ Pipeline completado")
            logger.info(f"💾 Reporte generado: {ruta_reporte.name}")
            
            # Analizar resultados
            estados = {}
            for resultado in resultados:
                estado = resultado["estado"]
                estados[estado] = estados.get(estado, 0) + 1
            
            logger.info(f"📊 Resumen de estados:")
            for estado, cantidad in estados.items():
                logger.info(f"   {estado}: {cantidad}")
            
            # Alertas de descuadres
            errores = [r for r in resultados if r["estado"] == "ERROR"]
            if errores:
                logger.warning(f"⚠️ {len(errores)} archivo(s) con ERROR:")
                for error in errores:
                    logger.warning(f"   - {error['nombre']}: {error['mensaje']}")
            
            revisiones = [r for r in resultados if r["estado"] == "REVISAR"]
            if revisiones:
                logger.info(f"📋 {len(revisiones)} archivo(s) requieren revisión:")
                for revision in revisiones:
                    logger.info(f"   - {revision['nombre']}: {revision['mensaje']}")
            
            logger.info("=" * 70)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en ejecución del pipeline: {e}", exc_info=True)
            return False

    def programar(self):
        """Programa el pipeline para ejecutarse cada día a la hora especificada."""
        logger.info(f"📅 Pipeline programado para ejecutarse diariamente a las {self.hora}")

    def _proxima_ejecucion(self, ahora: datetime) -> datetime:
        """Calcula la próxima ejecución diaria, incluso tras medianoche."""
        hora, minuto = (int(parte) for parte in self.hora.split(":"))
        proxima = ahora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
        if proxima <= ahora:
            proxima += timedelta(days=1)
        return proxima

    def iniciar_servicio(self):
        """Inicia el servicio de planificación (bloquea el hilo)."""
        logger.info("▶️ Iniciando servicio de planificación...")
        logger.info("Presiona Ctrl+C para detener.")
        
        try:
            while True:
                proxima = self._proxima_ejecucion(datetime.now())
                espera = max(1, (proxima - datetime.now()).total_seconds())
                logger.info(f"⏳ Próxima ejecución: {proxima:%Y-%m-%d %H:%M}")
                time.sleep(espera)
                self.ejecutar_pipeline()
        except KeyboardInterrupt:
            logger.info("\n⏹️ Servicio detenido.")
            sys.exit(0)

    def ejecutar_ahora(self):
        """Ejecuta el pipeline inmediatamente."""
        logger.info("⚡ Ejecución inmediata solicitada")
        return self.ejecutar_pipeline()

    # ──────────────────────────────────────────────────────────

    def instalar_windows_task_scheduler(self):
        """Instala como tarea en Windows Task Scheduler."""
        logger.info("📋 Generando configuración para Windows Task Scheduler...")
        
        script_path = Path(__file__).resolve()
        python_exe = sys.executable
        
        # Comando a ejecutar
        comando = f'"{python_exe}" "{script_path}" --run'
        
        # Crear archivo batch para instalar
        batch_file = Path(__file__).parent / "instalar_scheduler.bat"
        
        batch_content = f"""@echo off
REM Crear tarea programada en Windows Task Scheduler
REM Requiere permisos de administrador

echo Instalando tarea: "Sofland Cierre Contable"...

schtasks /create /tn "Sofland Cierre Contable" /tr "{comando}" /sc daily /st 06:00 /f

if %ERRORLEVEL%==0 (
    echo Tarea creada exitosamente.
    echo Se ejecutara diariamente a las 06:00 AM.
) else (
    echo Error al crear la tarea. Asegurate de ejecutar como administrador.
)

pause
"""
        
        batch_file.write_text(batch_content)
        logger.info(f"✅ Generado: {batch_file.name}")
        logger.info("   Ejecuta como administrador para instalar la tarea")

    def instalar_cron_linux(self):
        """Genera configuración para cron en Linux/Mac."""
        logger.info("📋 Generando configuración para cron...")
        
        script_path = Path(__file__).resolve()
        python_exe = sys.executable
        
        cron_entry = f"0 6 * * * {python_exe} {script_path} --run"
        
        cron_file = Path(__file__).parent / "instalar_cron.sh"
        cron_content = f"""#!/bin/bash
# Instalar en crontab

echo "Agregando entrada a crontab..."
(crontab -l 2>/dev/null; echo "{cron_entry}") | crontab -

echo "✅ Tarea instalada en cron"
echo "Se ejecutará diariamente a las 06:00 AM"
echo ""
echo "Para verificar: crontab -l"
echo "Para editar: crontab -e"
echo "Para eliminar: crontab -r"
"""
        
        cron_file.write_text(cron_content)
        os.chmod(cron_file, 0o755)
        logger.info(f"✅ Generado: {cron_file.name}")
        logger.info("   Ejecuta: bash instalar_cron.sh")


# ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Planificador de tareas contables para Sofland"
    )
    parser.add_argument(
        "--time",
        type=validar_hora,
        default="06:00",
        help="Hora de ejecución diaria (HH:MM, default: 06:00)"
    )
    parser.add_argument(
        "--entrada",
        default="ejemplos",
        help="Directorio con archivos a procesar"
    )
    parser.add_argument(
        "--salida",
        default="reportes",
        help="Directorio para guardar reportes"
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Ejecutar pipeline ahora"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Iniciar servicio de planificación (ejecutar diariamente)"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Instalar en Windows Task Scheduler"
    )
    parser.add_argument(
        "--install-cron",
        action="store_true",
        help="Instalar en cron (Linux/Mac)"
    )
    
    args = parser.parse_args()
    
    # Crear planificador
    scheduler = SchedulerContable(
        directorio_entrada=args.entrada,
        directorio_salida=args.salida,
        hora_ejecucion=args.time
    )
    
    # Ejecutar acción
    if args.run:
        scheduler.ejecutar_ahora()
    elif args.watch:
        scheduler.programar()
        scheduler.iniciar_servicio()
    elif args.install:
        scheduler.instalar_windows_task_scheduler()
    elif args.install_cron:
        scheduler.instalar_cron_linux()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

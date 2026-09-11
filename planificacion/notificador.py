"""
Notificaciones del pipeline contable.

Por seguridad, el modo predeterminado es simulacion: registra el mensaje pero
no envia correo. Para habilitar SMTP se debe indicar --enviar y configurar las
variables SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD y ALERTA_EMAIL.
"""

from __future__ import annotations

import argparse
import logging
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


logger = logging.getLogger(__name__)


class NotificadorContable:
    """Construye y envia alertas sobre el resultado del pipeline."""

    def __init__(self, enviar: bool = False):
        self.enviar = enviar
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.destinatario = os.getenv("ALERTA_EMAIL", "")

    def construir_mensaje(self, resultados: list[dict], ruta_reporte: Path) -> EmailMessage:
        """Construye un correo con el resumen y los archivos que requieren accion."""
        errores = [r for r in resultados if r["estado"] == "ERROR"]
        revisiones = [r for r in resultados if r["estado"] == "REVISAR"]
        listos = [r for r in resultados if r["estado"] == "LISTO"]

        mensaje = EmailMessage()
        mensaje["Subject"] = (
            f"Sofland: {len(errores)} errores, {len(revisiones)} revisiones"
        )
        mensaje["From"] = self.smtp_user or "sofland-pipeline@localhost"
        mensaje["To"] = self.destinatario or "revision-contable@localhost"

        lineas = [
            "Resumen automatico del pipeline contable",
            "",
            f"Archivos listos: {len(listos)}",
            f"Archivos para revisar: {len(revisiones)}",
            f"Archivos con error: {len(errores)}",
            f"Reporte: {ruta_reporte}",
            "",
            "Archivos que requieren accion:",
        ]
        lineas.extend(
            f"- [{resultado['estado']}] {resultado['nombre']}: {resultado['mensaje']}"
            for resultado in errores + revisiones
        )
        mensaje.set_content("\n".join(lineas))
        return mensaje

    def notificar_resultados(self, resultados: list[dict], ruta_reporte: Path) -> bool:
        """Registra o envia la alerta segun la configuracion seleccionada."""
        mensaje = self.construir_mensaje(resultados, ruta_reporte)

        if not self.enviar:
            logger.info("Notificacion en simulacion; no se envio correo.")
            logger.info("Asunto: %s", mensaje["Subject"])
            return True

        configuracion = {
            "SMTP_HOST": self.smtp_host,
            "SMTP_USER": self.smtp_user,
            "SMTP_PASSWORD": self.smtp_password,
            "ALERTA_EMAIL": self.destinatario,
        }
        faltantes = [nombre for nombre, valor in configuracion.items() if not valor]
        if faltantes:
            raise RuntimeError(
                "Faltan variables SMTP para enviar: " + ", ".join(faltantes)
            )

        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as servidor:
            servidor.starttls()
            servidor.login(self.smtp_user, self.smtp_password)
            servidor.send_message(mensaje)

        logger.info("Notificacion enviada a %s", self.destinatario)
        return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Prueba de notificaciones del pipeline")
    parser.add_argument("--reporte", required=True, help="Ruta del reporte generado")
    parser.add_argument("--enviar", action="store_true", help="Enviar por SMTP")
    args = parser.parse_args()

    reporte = Path(args.reporte)
    notificador = NotificadorContable(enviar=args.enviar)
    notificador.notificar_resultados([], reporte)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
#!/bin/bash
# ──────────────────────────────────────────────────────────────
# detener.sh
# Script para detener el sistema en Linux y macOS
# ──────────────────────────────────────────────────────────────

echo "========================================================"
echo "    Deteniendo el Sistema de Contabilidad..."
echo "========================================================"
echo ""

docker compose down

echo ""
echo "✅ Sistema detenido correctamente."
echo "Puedes volver a iniciarlo ejecutando: ./instalar_y_ejecutar.sh"
echo "========================================================"

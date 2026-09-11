#!/bin/bash
# ──────────────────────────────────────────────────────────────
# instalar_y_ejecutar.sh
# Script para iniciar el sistema en Linux y macOS
# ──────────────────────────────────────────────────────────────

echo "========================================================"
echo "    SISTEMA DE CONTABILIDAD SOFLAND — JOCELYN"
echo "    Instalador automático para Mac/Linux"
echo "========================================================"
echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ ERROR: Docker no está instalado."
    echo "Por favor instala Docker Desktop: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Verificar si Docker está corriendo
if ! docker info &> /dev/null; then
    echo "❌ ERROR: Docker está instalado pero el demonio no está en ejecución."
    echo "Abre la aplicación Docker Desktop y vuelve a intentarlo."
    exit 1
fi

echo "[1/3] Construyendo el sistema..."
docker compose build

if [ $? -ne 0 ]; then
    echo "❌ Error al construir la imagen de Docker."
    exit 1
fi

echo "[2/3] Iniciando los contenedores..."
docker compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Error al levantar los contenedores."
    exit 1
fi

echo ""
echo "✅ SISTEMA INICIADO CORRECTAMENTE"
echo ""
echo "[3/3] Abriendo en el navegador: http://localhost:8501"

# Intentar abrir el navegador según el SO
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:8501" # Linux
elif command -v open &> /dev/null; then
    open "http://localhost:8501" # macOS
else
    echo "Por favor abre manualmente en tu navegador: http://localhost:8501"
fi

echo ""
echo "Para DETENER el sistema cuando termines, ejecuta: ./detener.sh"
echo "========================================================"

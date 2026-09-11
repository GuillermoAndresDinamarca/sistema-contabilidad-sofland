# ─────────────────────────────────────────────────────
# Dockerfile — Sistema de Contabilidad Sofland / Jocelyn
# ─────────────────────────────────────────────────────
# Imagen base liviana con Python 3.12
FROM python:3.12-slim

# Metadatos
LABEL maintainer="Capacitación Contabilidad"
LABEL description="Sistema de automatización contable para el área de remuneraciones"
LABEL version="1.0"

# Variables de entorno para Streamlit
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_THEME_BASE=light \
    STREAMLIT_THEME_PRIMARY_COLOR=#2563EB

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias primero (aprovecha caché de Docker)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app/ .

# Copiar ejemplos dentro del contenedor para demo inmediata
COPY ejemplos/ /app/ejemplos/

# Exponer el puerto de Streamlit
EXPOSE 8501

# Verificación de salud del contenedor
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Comando de inicio
CMD ["streamlit", "run", "app_gui.py", "--server.port=8501", "--server.address=0.0.0.0"]

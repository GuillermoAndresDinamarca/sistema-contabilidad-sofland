# Registro de Decisiones Arquitectónicas (ADR)

Este documento registra las decisiones técnicas importantes tomadas durante el desarrollo
del Sistema de Contabilidad Sofland, y el "por qué" detrás de ellas.

## ADR-001: Uso de Docker Desktop para Distribución

**Fecha:** 10 de Septiembre de 2026
**Estado:** Aceptado

**Contexto:**
El equipo de remuneraciones no sabe programar. Instalar Python, configurar entornos virtuales (`venv`), instalar dependencias de `pip` y ejecutar comandos por terminal generaría mucha fricción y errores de soporte.

**Decisión:**
Se decidió empaquetar toda la aplicación usando Docker. Se provee un archivo `INSTALAR.bat` que automatiza el proceso `docker compose build` y `docker compose up`. 

**Consecuencias Positivas:**
- Instalación de "cero toques" (One-Click) para el contador.
- Garantiza que la aplicación funcionará exactamente igual en cualquier PC.
- No ensucia el sistema operativo host con instalaciones de Python.

**Consecuencias Negativas:**
- Requiere que el usuario instale Docker Desktop previamente (se mitigó incluyendo el enlace de descarga en el script `.bat`).

---

## ADR-002: Streamlit como Framework de Interfaz Gráfica (GUI)

**Fecha:** 10 de Septiembre de 2026
**Estado:** Aceptado

**Contexto:**
Se requería una interfaz gráfica moderna, manejable solo con mouse, que pudiera soportar cargas pesadas de procesamiento de datos (Pandas) y mostrar gráficos interactivos.

**Decisión:**
Se eligió Streamlit sobre Tkinter, PyQt o una app web completa (React+Django).

**Consecuencias Positivas:**
- Desarrollo extremadamente rápido orientado a datos.
- Permite subir archivos Excel grandes (Dropzone) de forma nativa.
- Diseño web moderno responsivo "out-of-the-box".
- Fácil integración con Pandas para mostrar los Dataframes y Pivot Tables interactivas.

**Consecuencias Negativas:**
- El sistema corre en el navegador web local (`localhost:8501`) en lugar de ser un `.exe` nativo de Windows.

---

## ADR-003: Rechazo temprano de Kubernetes

**Fecha:** 10 de Septiembre de 2026
**Estado:** Aceptado

**Contexto:**
Se evaluó usar Kubernetes para orquestar los contenedores.

**Decisión:**
No usar Kubernetes en la Fase 1 ni Fase 2.

**Consecuencias Positivas:**
- Mantiene la arquitectura simple (un solo `docker-compose.yml`).
- Ahorra costos de infraestructura en la nube.
- No requiere conocimiento avanzado de DevOps por parte del equipo interno.

**Razón:** El equipo contable de Jocelyn son menos de 5 personas. Kubernetes añade una complejidad operacional injustificada para el volumen transaccional actual. Se reevaluará si la empresa escala a +50 contadores concurrentes.

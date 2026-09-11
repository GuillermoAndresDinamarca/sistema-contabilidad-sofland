@echo off
chcp 65001 >nul
title Sistema de Contabilidad Sofland — Instalador

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║     SISTEMA DE CONTABILIDAD SOFLAND — JOCELYN        ║
echo ║     Instalador automático para Windows               ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM ── Verificar si Docker Desktop está instalado ─────────────
echo [1/4] Verificando Docker Desktop...
docker --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo  ¡ATENCIÓN! Docker Desktop no está instalado en este equipo.
    echo.
    echo  Necesitas instalarlo una sola vez. Es gratuito.
    echo  Sigue estos pasos:
    echo.
    echo  1. Abre este enlace en tu navegador:
    echo     https://www.docker.com/products/docker-desktop/
    echo.
    echo  2. Descarga e instala Docker Desktop para Windows.
    echo.
    echo  3. Reinicia el computador cuando te lo pida.
    echo.
    echo  4. Vuelve a ejecutar este archivo (INSTALAR.bat).
    echo.
    start https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo     Docker Desktop detectado correctamente.
echo.

REM ── Verificar que Docker esté corriendo ──────────────────
echo [2/4] Verificando que Docker esté activo...
docker info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Docker está instalado pero no está en ejecución.
    echo  Busca "Docker Desktop" en el menú inicio y ábrelo.
    echo  Espera a que el ícono de la ballena aparezca en la barra de tareas.
    echo  Luego vuelve a ejecutar este archivo.
    echo.
    pause
    exit /b 1
)
echo     Docker está activo.
echo.

REM ── Construir la imagen (solo la primera vez o al actualizar) ──
echo [3/4] Construyendo el sistema (esto puede tomar 2-5 minutos la primera vez)...
echo       Las próximas veces será instantáneo.
echo.
docker compose build
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Hubo un error al construir el sistema.
    echo  Verifica tu conexión a internet e intenta de nuevo.
    pause
    exit /b 1
)
echo.
echo     Sistema construido correctamente.
echo.

REM ── Iniciar el sistema ────────────────────────────────────
echo [4/4] Iniciando el Sistema de Contabilidad...
docker compose up -d
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Hubo un error al iniciar el sistema.
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║  ✅  SISTEMA INICIADO CORRECTAMENTE                  ║
echo ║                                                      ║
echo ║  Abriendo en tu navegador...                        ║
echo ║  Si no abre, copia esta dirección en Chrome/Edge:  ║
echo ║                                                      ║
echo ║      http://localhost:8501                           ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM ── Esperar 3 segundos y abrir el navegador ───────────────
timeout /t 3 /nobreak >nul
start http://localhost:8501

echo  Para DETENER el sistema cuando termines:
echo  Ejecuta el archivo DETENER.bat
echo.
pause

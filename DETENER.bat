@echo off
chcp 65001 >nul
title Sistema de Contabilidad — Detener

echo.
echo Deteniendo el Sistema de Contabilidad Sofland...
docker compose down
echo.
echo ✅ Sistema detenido correctamente.
echo    Puedes volver a iniciarlo ejecutando INSTALAR.bat
echo.
pause
